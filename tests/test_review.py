import os
import zipfile
import io
import tempfile
from unittest.mock import patch
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from projects.models import Project
from requirements_app.models import Requirement
from reviews.models import Review, Finding
from projects.utils import validate_and_extract_zip, parse_srs_file, validate_zip_upload
from analyzer.services import RequirementMatcher, ScoreCalculator, ProjectAnalyzer, QualityChecker
from reviews.services import ReviewService

class ReviewSystemTestCase(TestCase):
    def setUp(self):
        self.mentor = User.objects.create_user(username='testmentor', password='password123', role=User.MENTOR)
        self.student = User.objects.create_user(username='teststudent', password='password123', role=User.STUDENT)
        self.client = APIClient()

    def test_requirement_keyword_matching(self):
        req = Requirement(requirement_id='REQ-001', description='System shall provide user login.', category='Authentication')
        source_files = {'views.py': 'def login_view(request): pass'}
        py_inspection = {'functions': [{'name': 'login_view', 'file': 'views.py', 'line': 1}], 'classes': []}

        match = RequirementMatcher.match_requirement(req, source_files, py_inspection)
        self.assertEqual(match['status'], 'Implemented')

    def test_score_calculator(self):
        scores = ScoreCalculator.calculate([], 100.0, {'has_tests': True, 'test_files_count': 2, 'has_readme': True})
        self.assertEqual(scores['overall_score'], 100)

    def test_api_login(self):
        response = self.client.post('/api/login/', {'username': 'testmentor', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['role'], User.MENTOR)

    def test_api_login_uses_unauthorized_status_for_invalid_credentials(self):
        response = self.client.post('/api/login/', {'username': 'testmentor', 'password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_projects_permissions(self):
        # Unauthenticated request
        response = self.client.get('/api/projects/')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Student request
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_project_creation_requires_student_owner_and_assigns_mentor(self):
        self.client.force_authenticate(user=self.mentor)
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, 'w') as bundle:
            bundle.writestr('main.py', 'print("hello")')
        data = {
            'name': 'API project', 'owner_id': str(self.student.pk),
            'zip_file': SimpleUploadedFile('project.zip', archive.getvalue(), content_type='application/zip'),
            'srs_file': SimpleUploadedFile('requirements.txt', b'Users shall log in.', content_type='text/plain'),
        }
        response = self.client.post(reverse('api_projects'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(pk=response.data['id'])
        self.assertEqual(project.owner, self.student)
        self.assertEqual(project.assigned_mentor, self.mentor)

    def test_project_upload_form_requires_a_student_owner(self):
        self.client.force_login(self.mentor)
        response = self.client.get(reverse('upload_project'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Choose the student or intern')

    def test_parse_srs_file_csv_with_header(self):
        csv_content = "req_id,description,category,priority\nREQ-001,System shall authenticate users,Authentication,High\nREQ-002,Store items in database,Database,Medium\n"
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_content)
            temp_path = f.name

        try:
            reqs = parse_srs_file(temp_path)
            self.assertEqual(len(reqs), 2)
            self.assertEqual(reqs[0]['req_id'], 'REQ-001')
            self.assertEqual(reqs[0]['description'], 'System shall authenticate users')
            self.assertEqual(reqs[0]['category'], 'Authentication')
            self.assertEqual(reqs[0]['priority'], 'High')
            self.assertEqual(reqs[1]['req_id'], 'REQ-002')
        finally:
            os.remove(temp_path)

    def test_parse_srs_file_csv_positional(self):
        csv_content = "REQ-010,API must expose data endpoint,API,High\n"
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_content)
            temp_path = f.name

        try:
            reqs = parse_srs_file(temp_path)
            self.assertEqual(len(reqs), 1)
            self.assertEqual(reqs[0]['req_id'], 'REQ-010')
            self.assertEqual(reqs[0]['description'], 'API must expose data endpoint')
        finally:
            os.remove(temp_path)

    def test_project_analyzer_scans_csv(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_file = os.path.join(tmp_dir, 'dataset.csv')
            with open(csv_file, 'w', encoding='utf-8') as f:
                f.write('col1,col2\nval1,val2\n')

            scanned = ProjectAnalyzer.scan_files(tmp_dir)
            self.assertIn('dataset.csv', scanned)
            self.assertIn('val1,val2', scanned['dataset.csv'])

    def test_requirement_without_searchable_terms_needs_manual_review(self):
        req = Requirement(requirement_id='REQ-LOW', description='A / I', category='General')
        result = RequirementMatcher.match_requirement(req, {}, {'functions': [], 'classes': []})
        self.assertEqual(result['status'], 'Manual Review')

    def test_quality_checker_reports_repeated_source_lines(self):
        repeated = '    return normalize_user_profile(record)\n'
        score, findings = QualityChecker.check_quality(
            {'one.py': repeated, 'two.py': repeated},
            {'py_files_count': 2, 'functions': [], 'variables': [], 'has_exception_handling': False, 'has_readme': False},
        )
        self.assertLess(score, 100)
        self.assertTrue(any(item['title'] == 'Repeated Source Lines' for item in findings))

    def test_zip_validation_rejects_traversal_and_executable_files(self):
        for name in ('../outside.py', 'setup.exe'):
            archive = io.BytesIO()
            with zipfile.ZipFile(archive, 'w') as bundle:
                bundle.writestr(name, 'unsafe')
            upload = SimpleUploadedFile('project.zip', archive.getvalue(), content_type='application/zip')
            with self.subTest(name=name), self.assertRaises(ValidationError):
                validate_zip_upload(upload)

    def test_mentor_cannot_view_another_mentors_project(self):
        assigned = Project.objects.create(
            name='Assigned project', owner=self.student, assigned_mentor=self.mentor, zip_file='zips/assigned.zip'
        )
        other_mentor = User.objects.create_user(username='othermentor', password='password123', role=User.MENTOR)
        self.client.force_login(other_mentor)
        response = self.client.get(reverse('project_detail', args=[assigned.pk]))
        self.assertEqual(response.status_code, 403)

    def test_assigned_mentor_sees_project_ai_review_options(self):
        project = Project.objects.create(
            name='Assigned project', owner=self.student, assigned_mentor=self.mentor, zip_file='zips/assigned.zip'
        )
        self.client.force_login(self.mentor)
        response = self.client.get(reverse('project_detail', args=[project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Optional AI-assisted review')

    def test_api_hides_projects_from_unassigned_mentors(self):
        assigned = Project.objects.create(
            name='Assigned project', owner=self.student, assigned_mentor=self.mentor, zip_file='zips/assigned.zip'
        )
        other_mentor = User.objects.create_user(username='api-othermentor', password='password123', role=User.MENTOR)
        self.client.force_authenticate(user=other_mentor)
        response = self.client.get(reverse('api_project_detail', args=[assigned.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mentor_can_archive_and_restore_assigned_project(self):
        project = Project.objects.create(
            name='Archive me', owner=self.student, assigned_mentor=self.mentor, zip_file='zips/archive.zip'
        )
        self.client.force_login(self.mentor)
        response = self.client.post(reverse('archive_project', args=[project.pk]))
        self.assertEqual(response.status_code, 302)
        project.refresh_from_db()
        self.assertTrue(project.is_archived)
        self.client.post(reverse('archive_project', args=[project.pk]))
        project.refresh_from_db()
        self.assertFalse(project.is_archived)

    def test_project_review_saves_optional_ai_feedback_with_srs_context(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            archive = io.BytesIO()
            with zipfile.ZipFile(archive, 'w') as bundle:
                bundle.writestr('main.py', 'def login_user(username):\n    return username\n')
                bundle.writestr('README.md', 'Login project')
            project = Project.objects.create(
                name='AI project', owner=self.student, assigned_mentor=self.mentor,
                zip_file=SimpleUploadedFile('source.zip', archive.getvalue(), content_type='application/zip'),
            )
            requirement = Requirement.objects.create(
                project=project, requirement_id='REQ-AI', description='The system shall support user login.', category='Authentication'
            )
            with patch('reviews.services._ask_ai', return_value='## Findings\nNo supported bugs found.') as ask_ai:
                review = ReviewService.run_review(project, self.mentor, ai_provider='local', ai_model='qwen2.5-coder:1.5b-instruct')
            review.refresh_from_db()
            self.assertEqual(review.ai_provider, 'local')
            self.assertIn('No supported bugs', review.ai_review)
            self.assertEqual(ask_ai.call_args.kwargs['requirements'][0]['id'], requirement.requirement_id)
            self.client.force_login(self.mentor)
            response = self.client.get(reverse('review_report', args=[project.pk, review.pk]))
            self.assertContains(response, 'No supported bugs')
