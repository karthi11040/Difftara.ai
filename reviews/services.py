import os
import logging
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from projects.utils import validate_and_extract_zip, parse_srs_file
from projects.models import Project
from requirements_app.models import Requirement
from reviews.models import Review, Finding, MentorReview
from activities.models import ActivityService
from analyzer.services import ProjectAnalyzer, RequirementMatcher, QualityChecker, ScoreCalculator

logger = logging.getLogger(__name__)

class ReviewService:
    @staticmethod
    def run_review(project, mentor_user=None):
        """
        Executes the full automated review pipeline for a given Project.
        """
        project.status = 'processing'
        project.save()

        try:
            # 1. Zip extraction
            zip_path = project.zip_file.path
            extract_target_dir = os.path.join(settings.MEDIA_ROOT, 'extracted', str(project.id))
            extracted_path = validate_and_extract_zip(zip_path, extract_target_dir)
            project.extracted_path = extracted_path
            project.save()

            # 2. SRS requirements processing
            requirements = list(project.requirements.filter(active=True))
            if not requirements and project.srs_file:
                extracted_reqs = parse_srs_file(project.srs_file.path)
                for req_data in extracted_reqs:
                    req_obj, _ = Requirement.objects.get_or_create(
                        project=project,
                        requirement_id=req_data['req_id'],
                        defaults={
                            'description': req_data['description'],
                            'category': req_data['category'],
                            'priority': req_data['priority']
                        }
                    )
                    requirements.append(req_obj)

            if not requirements:
                raise ValidationError('No requirements were found. Add requirements manually and run the review again.')

            # 3. Source code scanning & inspection
            source_files = ProjectAnalyzer.scan_files(extracted_path)
            py_inspection = ProjectAnalyzer.inspect_python_code(source_files)

            # 4. Quality checks
            quality_score, quality_findings = QualityChecker.check_quality(source_files, py_inspection)

            with transaction.atomic():
                # 5. Create Review object
                review = Review.objects.create(
                    project=project,
                    mentor=mentor_user,
                    status='completed',
                    overall_score=0,
                    compliance_score=0.0,
                    quality_score=quality_score,
                    testing_score=0.0,
                    doc_score=0.0
                )

                # 6. Requirement-to-code matching & create Findings
                req_findings_list = []
                for req in requirements:
                    match_result = RequirementMatcher.match_requirement(req, source_files, py_inspection)
                    finding = Finding.objects.create(
                        review=review,
                        requirement=req,
                        status=match_result['status'],
                        evidence_file=match_result['evidence_file'],
                        evidence_function=match_result['evidence_function'],
                        description=match_result['description'],
                        suggestion=match_result['suggestion'],
                        priority=match_result['priority']
                    )
                    req_findings_list.append(finding)

            # Add quality findings to review
                for q_finding in quality_findings:
                    Finding.objects.create(
                        review=review,
                        requirement=None,
                        status=q_finding['status'],
                        evidence_file=q_finding['evidence_file'],
                        evidence_function=q_finding['evidence_function'],
                        description=f"[{q_finding['category']}] {q_finding['title']}: {q_finding['description']}",
                        suggestion=q_finding['suggestion'],
                        priority=q_finding['priority']
                    )

            # 7. Calculate Scores
                scores = ScoreCalculator.calculate(req_findings_list, quality_score, py_inspection)
                review.compliance_score = scores['compliance_score']
                review.quality_score = scores['quality_score']
                review.testing_score = scores['testing_score']
                review.doc_score = scores['doc_score']
                review.overall_score = scores['overall_score']
                review.save()

            project.status = 'completed'
            project.save()

            if mentor_user:
                ActivityService.record(
                    user=mentor_user,
                    project=project,
                    action='REVIEW_RUN',
                    message=f"Completed automated review for project '{project.name}' with score {scores['overall_score']}%."
                )

            return review

        except Exception:
            project.status = 'failed'
            project.save()
            try:
                Review.objects.create(project=project, mentor=mentor_user, status='failed')
            except Exception:
                logger.exception('Could not save failed review history for project %s', project.pk)
            if mentor_user:
                ActivityService.record(
                    user=mentor_user,
                    project=project,
                    action='REVIEW_FAILED',
                    message=f"Review failed for project '{project.name}'. Check the server log for details."
                )
            raise

    @staticmethod
    def recalculate_review_score(review):
        """
        Recalculates review score taking into account mentor overrides!
        """
        req_findings = review.findings.filter(requirement__isnull=False)
        
        # Check source inspection data from previous run or evaluate
        source_files = ProjectAnalyzer.scan_files(review.project.extracted_path)
        py_inspection = ProjectAnalyzer.inspect_python_code(source_files)

        scores = ScoreCalculator.calculate(req_findings, review.quality_score, py_inspection)
        review.compliance_score = scores['compliance_score']
        review.overall_score = scores['overall_score']
        review.save()
        return review
