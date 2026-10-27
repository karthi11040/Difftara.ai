from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from projects.models import Project
from reviews.models import Finding, MentorReview, Review


class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student',
            password='password123',
            role=User.STUDENT,
        )
        self.other_student = User.objects.create_user(
            username='other-student',
            password='password123',
            role=User.STUDENT,
        )
        self.mentor = User.objects.create_user(
            username='mentor',
            password='password123',
            role=User.MENTOR,
        )

        self.student_project = Project.objects.create(
            name='Student project',
            owner=self.student,
            zip_file='zips/student-project.zip',
            status='completed',
        )
        self.other_project = Project.objects.create(
            name='Other project',
            owner=self.other_student,
            zip_file='zips/other-project.zip',
            status='completed',
        )

        self.student_review = Review.objects.create(
            project=self.student_project,
            mentor=self.mentor,
            overall_score=80,
        )
        self.other_review = Review.objects.create(
            project=self.other_project,
            mentor=self.mentor,
            overall_score=20,
        )
        Finding.objects.create(
            review=self.student_review,
            status='Missing',
            description='Missing requirement',
        )
        Finding.objects.create(
            review=self.student_review,
            status='Implemented',
            description='Implemented requirement',
        )
        Finding.objects.create(
            review=self.other_review,
            status='Missing',
            description='Private project finding',
        )

    def test_student_dashboard_only_aggregates_their_projects(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_projects'], 1)
        self.assertEqual(response.context['completed_count'], 1)
        self.assertEqual(response.context['avg_score'], 80)
        self.assertEqual(response.context['findings_to_inspect'], 1)
        self.assertContains(response, 'Student project')
        self.assertNotContains(response, 'Other project')

    def test_mentor_dashboard_includes_all_projects(self):
        self.client.force_login(self.mentor)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.context['total_projects'], 2)
        self.assertEqual(response.context['completed_count'], 2)
        self.assertEqual(response.context['avg_score'], 50)
        self.assertEqual(response.context['findings_to_inspect'], 2)

    def test_dashboard_finding_metric_respects_mentor_overrides(self):
        finding = Finding.objects.get(
            review=self.student_review,
            status='Missing',
        )
        MentorReview.objects.create(
            finding=finding,
            reviewer=self.mentor,
            original_status='Missing',
            final_status='Implemented',
        )
        self.client.force_login(self.student)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.context['findings_to_inspect'], 0)
