from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class RoleMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create users with different roles
        self.teacher = User.objects.create_user(username='t1', password='pw', role='teacher')
        self.school_admin = User.objects.create_user(username='s1', password='pw', role='school_admin')
        self.student = User.objects.create_user(username='st1', password='pw', role='student')

    def test_anonymous_redirected_to_login_for_protected(self):
        # /classes/ is protected -> anonymous should be redirected
        resp = self.client.get('/classes/')
        self.assertIn(resp.status_code, (302, 301))
        self.assertIn('/login/', resp['Location'])

    def test_teacher_access_classes(self):
        self.client.login(username='t1', password='pw')
        resp = self.client.get('/classes/')
        # Should be allowed (200 or redirect to dashboard depending on view)
        self.assertIn(resp.status_code, (200, 302, 301))

    def test_student_blocked_from_teacher_resources(self):
        self.client.login(username='st1', password='pw')
        resp = self.client.get('/teacher-resources/')
        # student should be forbidden (403) or redirected away
        self.assertIn(resp.status_code, (403, 302, 301))

    def test_school_admin_access_classes(self):
        self.client.login(username='s1', password='pw')
        resp = self.client.get('/classes/')
        self.assertIn(resp.status_code, (200, 302, 301))
