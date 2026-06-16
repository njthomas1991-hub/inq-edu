from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from core.models import School

User = get_user_model()


class AuthenticationTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        self.school = School.objects.create(name="Test School")

        self.teacher = User.objects.create_user(
            username="teacher1",
            email="teacher1@example.com",
            password="testpass123",
            role="teacher",
            school=self.school,
        )

        self.student = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="testpass123",
            role="student",
            school=self.school,
        )

        self.admin = User.objects.create_user(
            username="admin1",
            email="admin1@example.com",
            password="testpass123",
            role="school_admin",
            school=self.school,
            is_staff=True,
        )

    def test_teacher_dashboard_access(self):

        login_success = self.client.login(
            username="teacher1",
            password="testpass123",
        )

        self.assertTrue(login_success)

        response = self.client.get(reverse("teacher_dashboard"))

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_student_dashboard_access(self):

        login_success = self.client.login(
            username="student1",
            password="testpass123",
        )

        self.assertTrue(login_success)

        response = self.client.get(reverse("student_dashboard"))

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_admin_dashboard_access(self):

        login_success = self.client.login(
            username="admin1",
            password="testpass123",
        )

        self.assertTrue(login_success)

        response = self.client.get(reverse("school_admin_dashboard"))

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_login_required_redirect(self):

        response = self.client.get(reverse("teacher_dashboard"))

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_login_sets_success_message(self):

        response = self.client.post(
            reverse("account_login"),
            {
                "login": "teacher1@example.com",
                "password": "testpass123",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logged in successfully.")

    def test_logout_sets_success_message(self):

        self.client.login(username="teacher1", password="testpass123")

        response = self.client.post(
            reverse("account_logout"),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logged out successfully.")

    def test_profile_update_sets_success_message(self):

        self.client.login(username="teacher1", password="testpass123")

        response = self.client.post(
            reverse("profile"),
            {
                "display_name": "Teacher One",
                "first_name": "Teacher",
                "last_name": "One",
                "email": "teacher1@example.com",
                "school": self.school.pk,
                "bio": "Updated bio",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile updated successfully.")
