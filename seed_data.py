import os
import sys
import zipfile
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from projects.models import Project
from requirements_app.models import Requirement
from reviews.models import Review, Finding
from reviews.services import ReviewService

def create_sample_zip(zip_path):
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    with zipfile.ZipFile(zip_path, 'w') as zf:
        # README.md
        zf.writestr('README.md', '# Sample Student Library Portal\nThis project provides user login and library books management API.')

        # main app views.py
        views_code = """
import json
from django.http import JsonResponse

def login_view(request):
    \"\"\"Handles user authentication and login\"\"\"
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username and password:
            return JsonResponse({'status': 'authenticated', 'token': 'xyz123'})
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'message': 'Login page'})

def list_books(request):
    \"\"\"Fetches books from database\"\"\"
    books = [
        {'id': 1, 'title': 'Python 101', 'author': 'Guido'},
        {'id': 2, 'title': 'Django in Action', 'author': 'Adrian'}
    ]
    return JsonResponse({'books': books})

def upload_file_handler(request):
    try:
        file_obj = request.FILES.get('file')
        return JsonResponse({'status': 'uploaded'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
"""
        zf.writestr('app/views.py', views_code.strip())

        # models.py
        models_code = """
from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
"""
        zf.writestr('app/models.py', models_code.strip())

        # test_views.py
        tests_code = """
import unittest

class TestViews(unittest.TestCase):
    def test_login(self):
        self.assertTrue(True)

    def test_books_list(self):
        self.assertEqual(1 + 1, 2)
"""
        zf.writestr('tests/test_views.py', tests_code.strip())

    return zip_path

def seed():
    print("Seeding database...")
    # 1. Create Users
    sanjay_user, _ = User.objects.get_or_create(username='SanjayS', defaults={'email': 'sanjays@example.com', 'role': User.ADMIN})
    sanjay_user.set_password('Sanjay_8821')
    sanjay_user.is_superuser = True
    sanjay_user.is_staff = True
    sanjay_user.save()

    admin_user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'role': User.ADMIN})
    admin_user.set_password('Sanjay_8821')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()

    mentor_user, _ = User.objects.get_or_create(username='mentor', defaults={'email': 'mentor@example.com', 'role': User.MENTOR})
    mentor_user.set_password('Sanjay_8821')
    mentor_user.is_staff = True
    mentor_user.save()

    student_user, _ = User.objects.get_or_create(username='student', defaults={'email': 'student@example.com', 'role': User.STUDENT})
    student_user.set_password('Sanjay_8821')
    student_user.save()

    print("Created users: SanjayS (universal), admin, mentor, student")

    # 2. Create Sample Project
    zip_dir = os.path.join(django.conf.settings.MEDIA_ROOT, 'zips')
    zip_path = os.path.join(zip_dir, 'sample_library_app.zip')
    create_sample_zip(zip_path)

    project, created = Project.objects.get_or_create(
        name='Library Management API',
        defaults={
            'description': 'Intern submission for Library Management REST API with user login and database storage.',
            'owner': student_user,
            'zip_file': 'zips/sample_library_app.zip',
            'status': 'uploaded'
        }
    )

    if created:
        Requirement.objects.create(project=project, requirement_id='REQ-001', description='The system shall provide user login and authentication.', category='Authentication', priority='High')
        Requirement.objects.create(project=project, requirement_id='REQ-002', description='The system shall store data in SQLite database models.', category='Database', priority='High')
        Requirement.objects.create(project=project, requirement_id='REQ-003', description='The system shall expose REST API endpoints for books listing.', category='API', priority='High')
        Requirement.objects.create(project=project, requirement_id='REQ-004', description='The system shall handle file uploads securely.', category='File Handling', priority='Medium')

        print("Created sample project and requirements.")
        # Run review
        review = ReviewService.run_review(project, mentor_user=mentor_user)
        print(f"Executed automated review! Overall Score: {review.overall_score}%")

    try:
        from seed_25_projects import seed_25
        seed_25()
    except Exception as e:
        print(f"seed_25 error: {e}")

if __name__ == '__main__':
    seed()
