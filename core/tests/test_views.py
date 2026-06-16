from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Class, ClassStudent, School

User = get_user_model()


class ClassCRUDTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.teacher = User.objects.create_user(
            username="teacher1",
            password="testpass123",
            role="teacher",
        )

        self.client.login(username="teacher1", password="testpass123")

    def test_create_class(self):
        data = {
            "name": "New Math Class",
            "subject": "maths",
            "year_ks": "KS3",
            "description": "A new math class",
        }

        response = self.client.post(reverse("create_class"), data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Class.objects.filter(name="New Math Class").exists())

    def test_read_class_detail(self):
        class_obj = Class.objects.create(
            name="Detail Test Class",
            teacher=self.teacher,
            subject="english",
            year_ks="KS1",
        )

        response = self.client.get(reverse("class_detail", args=[class_obj.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail Test Class")

    def test_remove_student_from_class(self):
        student = User.objects.create_user(
            username="student1",
            password="testpass123",
            role="student",
        )

        class_obj = Class.objects.create(
            name="Test Class",
            teacher=self.teacher,
            subject="maths",
            year_ks="KS2",
        )

        ClassStudent.objects.create(
            student=student,
            clazz=class_obj,
        )

        response = self.client.post(
            reverse("remove_student", args=[class_obj.pk, student.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            ClassStudent.objects.filter(
                student=student,
                clazz=class_obj,
            ).exists()
        )


class ApiCurrentUserTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.school = School.objects.create(name="Test School")
        self.user = User.objects.create_user(
            username="teacher1",
            password="testpass123",
            role="teacher",
            school=self.school,
        )

    def test_current_user_api_returns_school_detail(self):
        self.client.login(username="teacher1", password="testpass123")

        response = self.client.get(reverse("api_current_user"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["school_detail"], {"name": "Test School"})
