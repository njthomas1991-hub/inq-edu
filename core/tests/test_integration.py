from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Class, School

User = get_user_model()


class TeacherWorkflowIntegrationTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.school = School.objects.create(name="Test School")

        self.teacher = User.objects.create_user(
            username="teacher1",
            password="testpass123",
            role="teacher",
            school=self.school,
        )

        self.client.login(username="teacher1", password="testpass123")

    def test_complete_class_creation_workflow(self):

        class_data = {
            "name": "Integration Test Class",
            "subject": "maths",
            "year_ks": "KS2",
            "description": "Test description",
        }

        response = self.client.post(
            reverse("create_class"),
            class_data,
        )

        self.assertEqual(response.status_code, 302)

        class_obj = Class.objects.get(name="Integration Test Class")

        self.assertEqual(class_obj.teacher, self.teacher)

        student_data = {
            "username": "teststudent1",
            "full_name": "Test Student",
            "year_ks": "KS2",
        }

        self.client.post(
            reverse("student_signup"),
            student_data,
        )

        response = self.client.get(reverse("class_detail", args=[class_obj.pk]))

        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("teacher_analytics"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Integration Test Class")
