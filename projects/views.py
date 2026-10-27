import os
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Avg, Prefetch, Q
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.http import require_POST
from accounts.models import User
from projects.models import Project
from requirements_app.models import Requirement
from reviews.models import Review, Finding, MentorReview
from activities.models import Activity, ActivityService
from reviews.services import ReviewService
from analyzer.services import ProjectAnalyzer
from projects.utils import validate_zip_upload, validate_srs_upload

logger = logging.getLogger(__name__)

@login_required
def dashboard_view(request):
    if request.user.is_mentor_user:
        project_queryset = Project.objects.all()
        review_queryset = Review.objects.all()
        activities = Activity.objects.all()[:15]
    else:
        project_queryset = Project.objects.filter(owner=request.user)
        review_queryset = Review.objects.filter(project__owner=request.user)
        activities = Activity.objects.filter(user=request.user)[:15]

    projects = list(
        project_queryset.order_by('-created_at').prefetch_related(
            Prefetch(
                'reviews',
                queryset=Review.objects.filter(status='completed').order_by('-created_at'),
                to_attr='dashboard_reviews',
            )
        )
    )
    for project in projects:
        project.latest_review = project.dashboard_reviews[0] if project.dashboard_reviews else None

    completed_reviews = review_queryset.filter(status='completed')
    avg_score = completed_reviews.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
    non_implemented_statuses = ['Partial', 'Missing', 'Manual Review']
    findings_to_inspect = Finding.objects.filter(review__in=completed_reviews).filter(
        Q(
            mentor_override__isnull=True,
            status__in=non_implemented_statuses,
        )
        | Q(mentor_override__final_status__in=non_implemented_statuses)
    ).count()

    context = {
        'projects': projects,
        'activities': activities,
        'total_projects': len(projects),
        'completed_count': completed_reviews.count(),
        'avg_score': int(round(avg_score)),
        'findings_to_inspect': findings_to_inspect,
    }
    return render(request, 'dashboard.html', context)

@login_required
def project_list_view(request):
    if request.user.is_mentor_user:
        project_queryset = Project.objects.all()
    else:
        project_queryset = Project.objects.filter(owner=request.user)
    projects = project_queryset.order_by('-created_at').prefetch_related(
        Prefetch('reviews', queryset=Review.objects.filter(status='completed').order_by('-created_at'), to_attr='list_reviews')
    )
    for project in projects:
        project.latest_review = project.list_reviews[0] if project.list_reviews else None
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def upload_project_view(request):
    if not request.user.is_mentor_user:
        messages.error(request, 'Only Mentors and Admins can upload projects.')
        return redirect('dashboard')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        zip_file = request.FILES.get('zip_file')
        srs_file = request.FILES.get('srs_file')
        manual_reqs = request.POST.getlist('req_desc')
        manual_ids = request.POST.getlist('req_id')
        manual_cats = request.POST.getlist('req_cat')
        students = User.objects.filter(role=User.STUDENT).order_by('username')

        def render_form():
            return render(request, 'upload_project.html', {
                'students': students,
                'form_data': {'name': name, 'description': description},
            })

        if not name or not zip_file:
            messages.error(request, 'Project name and ZIP file are required.')
            return render_form()
        if len(name) > 255:
            messages.error(request, 'Project name must be 255 characters or fewer.')
            return render_form()

        try:
            validate_zip_upload(zip_file)
            if srs_file:
                validate_srs_upload(srs_file)
        except ValidationError as exc:
            messages.error(request, exc.messages[0])
            return render_form()

        entered_requirements = [(i.strip(), d.strip(), c.strip()) for i, d, c in zip(manual_ids, manual_reqs, manual_cats) if d.strip()]
        if not entered_requirements and not srs_file:
            messages.error(request, 'Upload an SRS document or enter at least one requirement.')
            return render_form()
        used_ids = set()
        normalized_requirements = []
        for index, (req_id, req_desc, req_cat) in enumerate(entered_requirements, start=1):
            next_id = req_id or f'REQ-{index:03d}'
            next_number = index
            while not req_id and next_id in used_ids:
                next_number += 1
                next_id = f'REQ-{next_number:03d}'
            if len(next_id) > 50 or next_id in used_ids:
                messages.error(request, 'Requirement IDs must be unique and 50 characters or fewer.')
                return render_form()
            used_ids.add(next_id)
            normalized_requirements.append((next_id, req_desc, req_cat))
        entered_requirements = normalized_requirements

        owner = request.user
        owner_id = request.POST.get('owner_id')
        if owner_id:
            owner = get_object_or_404(User, pk=owner_id, role=User.STUDENT)

        try:
            with transaction.atomic():
                project = Project.objects.create(
                    name=name,
                    description=description,
                    owner=owner,
                    zip_file=zip_file,
                    srs_file=srs_file
                )

                for r_id, r_desc, r_cat in entered_requirements:
                    Requirement.objects.create(
                        project=project,
                        requirement_id=r_id,
                        description=r_desc,
                        category=r_cat or 'General'
                    )

            ActivityService.record(
                user=request.user,
                project=project,
                action='UPLOAD_PROJECT',
                message=f"Uploaded project ZIP '{project.name}' successfully."
            )

            messages.success(request, f"Project '{project.name}' uploaded successfully!")
            return redirect('project_detail', pk=project.id)

        except Exception:
            logger.exception('Project upload failed for user %s', request.user.pk)
            messages.error(request, 'The project could not be saved. Please try again.')

    return render(request, 'upload_project.html', {'students': User.objects.filter(role=User.STUDENT).order_by('username')})

@login_required
def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_mentor_user and project.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        if not request.user.is_mentor_user:
            raise PermissionDenied
        req_id = request.POST.get('requirement_id', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', '').strip() or 'General'
        priority = request.POST.get('priority', 'High')
        if not description or priority not in {'High', 'Medium', 'Low'}:
            messages.error(request, 'Enter a requirement and choose a valid priority.')
        elif len(req_id) > 50 or len(category) > 100:
            messages.error(request, 'Requirement ID and category are too long.')
        elif req_id and project.requirements.filter(requirement_id=req_id).exists():
            messages.error(request, 'That requirement ID already exists in this project.')
        else:
            next_number = project.requirements.count() + 1
            next_id = req_id or f'REQ-{next_number:03d}'
            while not req_id and project.requirements.filter(requirement_id=next_id).exists():
                next_number += 1
                next_id = f'REQ-{next_number:03d}'
            Requirement.objects.create(project=project, requirement_id=next_id, description=description, category=category, priority=priority)
            ActivityService.record(user=request.user, project=project, action='REQUIREMENT_ADD', message=f"Added requirement {next_id}.")
            messages.success(request, f'Requirement {next_id} added.')
            return redirect('project_detail', pk=pk)

    latest_review = project.reviews.filter(status='completed').order_by('-created_at').first()
    
    # Inspect files list if extracted
    files_tree = []
    if project.extracted_path and os.path.exists(project.extracted_path):
        source_files = ProjectAnalyzer.scan_files(project.extracted_path)
        files_tree = list(source_files.keys())

    context = {
        'project': project,
        'latest_review': latest_review,
        'requirements': project.requirements.filter(active=True),
        'files_tree': files_tree,
        'review_history': project.reviews.select_related('mentor').order_by('-created_at'),
    }
    return render(request, 'project_detail.html', context)

@login_required
@require_POST
def start_review_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_mentor_user:
        messages.error(request, 'Only Mentors and Admins can run reviews.')
        return redirect('project_detail', pk=pk)

    try:
        review = ReviewService.run_review(project, mentor_user=request.user)
        messages.success(request, f"Review completed! Overall Score: {review.overall_score}%")
        return redirect('project_findings', pk=pk)
    except ValidationError as exc:
        messages.error(request, exc.messages[0])
        return redirect('project_detail', pk=pk)
    except Exception:
        logger.exception('Review failed for project %s', project.pk)
        messages.error(request, 'The review failed unexpectedly. Check the uploaded files and try again.')
        return redirect('project_detail', pk=pk)

@login_required
def project_findings_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_mentor_user and project.owner != request.user:
        raise PermissionDenied
    review = project.reviews.filter(status='completed').order_by('-created_at').first()
    if not review:
        messages.warning(request, 'No review has been conducted yet for this project.')
        return redirect('project_detail', pk=pk)

    findings = review.findings.select_related('requirement', 'mentor_override__reviewer').all()

    if request.method == 'POST':
        if not request.user.is_mentor_user:
            raise PermissionDenied
        finding_id = request.POST.get('finding_id')
        final_status = request.POST.get('final_status')
        comment = request.POST.get('comment', '')
        is_correct_value = request.POST.get('is_correct', 'true').lower()
        if final_status not in dict(Finding.STATUS_CHOICES):
            messages.error(request, 'Choose a valid finding status.')
            return redirect('project_findings', pk=pk)
        if is_correct_value not in {'true', 'false'}:
            messages.error(request, 'Choose whether the automated finding is correct or incorrect.')
            return redirect('project_findings', pk=pk)

        finding = get_object_or_404(Finding, pk=finding_id, review=review)
        MentorReview.objects.update_or_create(
            finding=finding,
            defaults={
                'reviewer': request.user,
                'original_status': finding.status,
                'final_status': final_status,
                'comment': comment,
                'is_correct': is_correct_value == 'true',
            }
        )
        ReviewService.recalculate_review_score(review)
        ActivityService.record(
            user=request.user,
            project=project,
            action='MENTOR_OVERRIDE',
            message=f"Updated finding #{finding.id} status to '{final_status}'."
        )
        messages.success(request, 'Finding status override saved and score recalculated!')
        return redirect('project_findings', pk=pk)

    context = {
        'project': project,
        'review': review,
        'findings': findings
    }
    return render(request, 'findings.html', context)

@login_required
def project_report_view(request, pk, review_id=None):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_mentor_user and project.owner != request.user:
        raise PermissionDenied
    review = get_object_or_404(project.reviews.filter(status='completed'), pk=review_id) if review_id else project.reviews.filter(status='completed').order_by('-created_at').first()
    if not review:
        messages.warning(request, 'No report available yet.')
        return redirect('project_detail', pk=pk)

    findings = list(review.findings.select_related('requirement', 'mentor_override__reviewer').all())
    req_findings = [f for f in findings if f.requirement]
    status_map = {'Implemented': 1.0, 'Partial': 0.5, 'Missing': 0.0, 'Manual Review': 0.25}

    # 1. Automatic AI Score (original finding.status)
    if req_findings:
        auto_comp = (sum(status_map.get(f.status, 0.0) for f in req_findings) / len(req_findings)) * 100.0
    else:
        auto_comp = 100.0
    auto_overall = int(round((auto_comp * 0.60) + (review.quality_score * 0.20) + (review.testing_score * 0.10) + (review.doc_score * 0.10)))

    # 2. Manual Mentor Evaluated Score (finding.current_status with overrides)
    if req_findings:
        manual_comp = (sum(status_map.get(f.current_status, 0.0) for f in req_findings) / len(req_findings)) * 100.0
    else:
        manual_comp = 100.0
    manual_overall = int(round((manual_comp * 0.60) + (review.quality_score * 0.20) + (review.testing_score * 0.10) + (review.doc_score * 0.10)))

    score_delta = manual_overall - auto_overall
    has_overrides = any(hasattr(f, 'mentor_override') and f.mentor_override for f in findings)
    category_totals = {}
    for finding in req_findings:
        category = finding.requirement.category or 'General'
        category_totals.setdefault(category, []).append(status_map.get(finding.current_status, 0.0))
    category_scores = [
        {'name': name, 'score': round(sum(values) / len(values) * 100), 'count': len(values)}
        for name, values in sorted(category_totals.items())
    ]
    inspection = ProjectAnalyzer.inspect_python_code(ProjectAnalyzer.scan_files(project.extracted_path))
    previous_review = project.reviews.filter(status='completed', created_at__lt=review.created_at).order_by('-created_at').first()

    context = {
        'project': project,
        'review': review,
        'findings': findings,
        'req_findings': req_findings,
        'auto_compliance': round(auto_comp, 1),
        'auto_overall': auto_overall,
        'manual_compliance': round(manual_comp, 1),
        'manual_overall': manual_overall,
        'score_delta': score_delta,
        'has_overrides': has_overrides,
        'category_scores': category_scores,
        'testing_summary': f"{inspection['test_files_count']} test file(s) detected" if inspection['test_files_count'] else 'No test files were detected. Tests were not executed.',
        'documentation_summary': 'README or project documentation detected' if inspection['has_readme'] else 'No README or documentation file was detected.',
        'previous_review': previous_review,
        'score_change': manual_overall - previous_review.overall_score if previous_review else None,
    }
    return render(request, 'report.html', context)

@login_required
def activities_view(request):
    if request.user.is_mentor_user:
        activities = Activity.objects.all()[:100]
    else:
        activities = Activity.objects.filter(user=request.user)[:100]
    return render(request, 'activities.html', {'activities': activities})
