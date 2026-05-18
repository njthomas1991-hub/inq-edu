from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Class

User = get_user_model()


class FormValidationTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.teacher = User.objects.create_user(
            username="teacher1",
            password="testpass123",
            role="teacher",
        )

        self.client.login(username="teacher1", password="testpass123")

    def test_class_form_validation_missing_fields(self):
        data = {
            "name": "",
            "subject": "maths",
            "year_ks": 2,
        }

        response = self.client.post(reverse("create_class"), data)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(Class.objects.filter(subject="maths").exists())

    def test_class_form_validation_invalid_subject(self):
        data = {
            "name": "Test Class",
            "subject": "invalid_subject",
            "year_ks": 2,
        }

        self.client.post(reverse("create_class"), data)

        self.assertFalse(Class.objects.filter(name="Test Class").exists())
