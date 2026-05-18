from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from core.models import (
    Avatar,
    Class,
    ClassStudent,
    School,
    SchoolAnalyticsProfile,
)

User = get_user_model()


class UserModelTestCase(TestCase):

    def setUp(self):

        self.school = School.objects.create(name="Test School")

        self.teacher = User.objects.create_user(
            username="teacher1",
            email="teacher@school.com",
            password="testpass123",
            role="teacher",
            school=self.school,
        )

        self.student = User.objects.create_user(
            username="student1",
            email="student@school.com",
            password="testpass123",
            role="student",
            school=self.school,
        )

        self.admin = User.objects.create_user(
            username="admin1",
            email="admin@school.com",
            password="testpass123",
            role="school_admin",
            school=self.school,
        )

    def test_user_creation_with_role(self):
        self.assertEqual(self.teacher.role, "teacher")
        self.assertEqual(self.student.role, "student")
        self.assertEqual(self.admin.role, "school_admin")

    def test_user_school_assignment(self):
        self.assertEqual(self.teacher.school.name, "Test School")
        self.assertEqual(self.student.school.name, "Test School")
        self.assertEqual(self.admin.school.name, "Test School")

    def test_user_string_representation(self):
        self.assertEqual(str(self.teacher), "teacher1 (teacher)")


class ClassModelTestCase(TestCase):

    def setUp(self):

        self.school = School.objects.create(name="Test School")

        self.teacher = User.objects.create_user(
            username="teacher1",
            password="testpass123",
            role="teacher",
            school=self.school,
        )

        self.class1 = Class.objects.create(
            name="Math 101",
            teacher=self.teacher,
            subject="maths",
            year_ks=2,
            description="Year 2 Mathematics",
        )

        self.class2 = Class.objects.create(
            name="Science Advanced",
            teacher=self.teacher,
            subject="science",
            year_ks=3,
        )

    def test_class_creation(self):

        self.assertEqual(
            self.class1.name,
            "Math 101",
        )

        self.assertEqual(
            self.class1.teacher,
            self.teacher,
        )

        self.assertEqual(
            self.class1.subject,
            "maths",
        )

    def test_class_string_representation(self):

        self.assertEqual(
            str(self.class1),
            "Math 101",
        )


class ClassStudentModelTestCase(TestCase):

    def setUp(self):

        self.school = School.objects.create(name="Test School")

        self.teacher = User.objects.create_user(
            username="teacher1",
            password="testpass123",
            role="teacher",
            school=self.school,
        )

        self.student = User.objects.create_user(
            username="student1",
            password="testpass123",
            role="student",
            school=self.school,
        )

        self.class_obj = Class.objects.create(
            name="Test Class",
            teacher=self.teacher,
            subject="maths",
            year_ks=2,
        )

        self.enrollment = ClassStudent.objects.create(
            student=self.student,
            clazz=self.class_obj,
        )

    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.clazz, self.class_obj)

    def test_unique_enrollment(self):
        with self.assertRaises(IntegrityError):
            ClassStudent.objects.create(
                student=self.student,
                clazz=self.class_obj,
            )

    def test_enrollment_string_representation(self):
        expected = f"{self.student.username} -> {self.class_obj.name}"
        self.assertEqual(str(self.enrollment), expected)


class AvatarModelTestCase(TestCase):

    def setUp(self):

        self.school = School.objects.create(name="Test School")

        self.user = User.objects.create_user(
            username="student1",
            password="testpass123",
            role="student",
            school=self.school,
        )

        self.avatar = Avatar.objects.create(user=self.user)

    def test_avatar_creation(self):

        self.assertEqual(self.avatar.user, self.user)

    def test_avatar_has_default_config(self):

        self.assertIsInstance(self.avatar.avatar_config, dict)

    def test_avatar_string_representation(self):

        self.assertEqual(str(self.avatar), "student1's avatar")

    def test_one_avatar_per_user(self):

        with self.assertRaises(IntegrityError):

            Avatar.objects.create(user=self.user)


class SchoolAnalyticsProfileTestCase(TestCase):

    def setUp(self):

        self.school = School.objects.create(name="Test School")

        self.admin = User.objects.create_user(
            username="admin1",
            password="testpass123",
            role="school_admin",
            school=self.school,
        )

    def test_profile_creation(self):

        profile = SchoolAnalyticsProfile.objects.create(
            school=self.school,
        )

        self.assertEqual(
            profile.school.name,
            "Test School",
        )
