import os
import zipfile
import tempfile
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from projects.models import Project
from requirements_app.models import Requirement
from reviews.models import Review, Finding
from projects.utils import validate_and_extract_zip, parse_srs_file
from analyzer.services import RequirementMatcher, ScoreCalculator, ProjectAnalyzer

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

    def test_api_projects_permissions(self):
        # Unauthenticated request
        response = self.client.get('/api/projects/')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Student request
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
