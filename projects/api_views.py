import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from accounts.models import User
from projects.models import Project
from reviews.models import Review, Finding, MentorReview
from activities.models import Activity, ActivityService
from reviews.services import ReviewService
from projects.serializers import (
    UserSerializer, ProjectSerializer, RequirementSerializer, 
    ReviewSerializer, FindingSerializer, ActivitySerializer
)

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def api_projects(request):
    if request.method == 'GET':
        if request.user.is_mentor_user:
            projects = Project.objects.all().order_by('-created_at')
        else:
            projects = Project.objects.filter(owner=request.user).order_by('-created_at')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_mentor_user:
            return Response({'error': 'Only mentors and admins can create/upload projects'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(owner=request.user)
            ActivityService.record(
                user=request.user,
                project=project,
                action='CREATE_PROJECT',
                message=f"Created project '{project.name}' and uploaded ZIP package."
            )
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_mentor_user and project.owner != request.user:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProjectSerializer(project)
    data = serializer.data
    
    # Attach recent review
    latest_review = project.reviews.filter(status='completed').order_by('-created_at').first()
    if latest_review:
        data['latest_review'] = ReviewSerializer(latest_review).data
        
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_start_review(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_mentor_user:
        return Response({'error': 'Only mentors and admins can initiate reviews'}, status=status.HTTP_403_FORBIDDEN)

    try:
        review = ReviewService.run_review(project, mentor_user=request.user)
        return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)
    except ValidationError as exc:
        return Response({'error': exc.messages[0]}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        logger.exception('API review failed for project %s', project.pk)
        return Response({'error': 'Review failed unexpectedly. Check the uploaded files and try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_findings(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_mentor_user and project.owner_id != request.user.id:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    review = project.reviews.filter(status='completed').order_by('-created_at').first()
    if not review:
        return Response({'error': 'No review found for this project'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = FindingSerializer(review.findings.all(), many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_save_mentor_review(request, finding_pk):
    if not request.user.is_mentor_user:
        return Response({'error': 'Only mentors and admins can override findings'}, status=status.HTTP_403_FORBIDDEN)

    finding = get_object_or_404(Finding, pk=finding_pk)
    final_status = request.data.get('final_status')
    comment = request.data.get('comment', '')
    is_correct = request.data.get('is_correct', True)

    if final_status not in ['Implemented', 'Partial', 'Missing', 'Manual Review']:
        return Response({'error': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)
    if not isinstance(is_correct, bool):
        return Response({'error': 'is_correct must be a boolean value'}, status=status.HTTP_400_BAD_REQUEST)

    mentor_override, created = MentorReview.objects.update_or_create(
        finding=finding,
        defaults={
            'reviewer': request.user,
            'original_status': finding.status,
            'final_status': final_status,
            'comment': comment,
            'is_correct': is_correct
        }
    )

    # Recalculate overall score for the review!
    ReviewService.recalculate_review_score(finding.review)

    ActivityService.record(
        user=request.user,
        project=finding.review.project,
        action='MENTOR_OVERRIDE',
        message=f"Mentor overridden finding #{finding.id} status from '{finding.status}' to '{final_status}'."
    )

    return Response(FindingSerializer(finding).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_report(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_mentor_user and project.owner_id != request.user.id:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    review = project.reviews.filter(status='completed').order_by('-created_at').first()
    if not review:
        return Response({'error': 'No review report available yet.'}, status=status.HTTP_404_NOT_FOUND)

    report_payload = {
        'project_id': project.id,
        'project_name': project.name,
        'owner': project.owner.username,
        'created_at': project.created_at,
        'overall_score': review.overall_score,
        'compliance_score': review.compliance_score,
        'quality_score': review.quality_score,
        'testing_score': review.testing_score,
        'doc_score': review.doc_score,
        'mentor': review.mentor.username if review.mentor else 'Automated',
        'findings': FindingSerializer(review.findings.all(), many=True).data
    }
    return Response(report_payload)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_activities(request):
    if request.user.is_mentor_user:
        activities = Activity.objects.all()[:50]
    else:
        activities = Activity.objects.filter(user=request.user)[:50]
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)
