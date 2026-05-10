from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Class, ClassStudent, Avatar, SchoolAnalyticsProfile, TeachingResource, ForumPost

User = get_user_model()


# ============================================================================
# MODEL TESTS
# ============================================================================

class UserModelTestCase(TestCase):
    """Test custom User model functionality"""
    
    def setUp(self):
        """Create test users"""
        self.teacher = User.objects.create_user(
            username='teacher1',
            email='teacher@school.com',
            password='testpass123',
            role='teacher',
            school='Test School'
        )
        self.student = User.objects.create_user(
            username='student1',
            email='student@school.com',
            password='testpass123',
            role='student',
            school='Test School'
        )
        self.admin = User.objects.create_user(
            username='admin1',
            email='admin@school.com',
            password='testpass123',
            role='school_admin',
            school='Test School'
        )
    
    def test_user_creation_with_role(self):
        """Test that users are created with correct roles"""
        self.assertEqual(self.teacher.role, 'teacher')
        self.assertEqual(self.student.role, 'student')
        self.assertEqual(self.admin.role, 'school_admin')
    
    def test_user_school_assignment(self):
        """Test that users are assigned to correct school"""
        self.assertEqual(self.teacher.school, 'Test School')
        self.assertEqual(self.student.school, 'Test School')
    
    def test_user_string_representation(self):
        """Test User __str__ method"""
        self.assertEqual(str(self.teacher), 'teacher1')


class ClassModelTestCase(TestCase):
    """Test Class model functionality"""
    
    def setUp(self):
        """Create test teacher and classes"""
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher',
            school='Test School'
        )
        self.class1 = Class.objects.create(
            name='Math 101',
            teacher=self.teacher,
            subject='maths',
            year_ks=2,
            description='Year 2 Mathematics'
        )
        self.class2 = Class.objects.create(
            name='Science Advanced',
            teacher=self.teacher,
            subject='science',
            year_ks=3
        )
    
    def test_class_creation(self):
        """Test that classes are created correctly"""
        self.assertEqual(self.class1.name, 'Math 101')
        self.assertEqual(self.class1.teacher, self.teacher)
        self.assertEqual(self.class1.subject, 'maths')
    
    def test_key_stage_label(self):
        """Test key_stage_label property"""
        self.assertEqual(self.class1.key_stage_label, 'KS2')
        self.assertEqual(self.class2.key_stage_label, 'KS3')
    
    def test_subject_label(self):
        """Test subject_label property"""
        self.assertEqual(self.class1.subject_label, 'Mathematics')
        self.assertEqual(self.class2.subject_label, 'Science')
    
    def test_class_string_representation(self):
        """Test Class __str__ method"""
        self.assertEqual(str(self.class1), 'Math 101')


class ClassStudentModelTestCase(TestCase):
    """Test ClassStudent enrollment model"""
    
    def setUp(self):
        """Create test data for enrollment"""
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher'
        )
        self.student = User.objects.create_user(
            username='student1',
            password='testpass123',
            role='student'
        )
        self.class_obj = Class.objects.create(
            name='Test Class',
            teacher=self.teacher,
            subject='maths',
            year_ks=2
        )
        self.enrollment = ClassStudent.objects.create(
            student=self.student,
            clazz=self.class_obj
        )
    
    def test_enrollment_creation(self):
        """Test student enrollment in class"""
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.clazz, self.class_obj)
        self.assertIsNotNone(self.enrollment.added_at)
    
    def test_unique_enrollment(self):
        """Test that duplicate enrollments are prevented"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            ClassStudent.objects.create(
                student=self.student,
                clazz=self.class_obj
            )
    
    def test_enrollment_string_representation(self):
        """Test ClassStudent __str__ method"""
        expected = f"{self.student.username} in {self.class_obj.name}"
        self.assertEqual(str(self.enrollment), expected)


class AvatarModelTestCase(TestCase):
    """Test Avatar model functionality"""
    
    def setUp(self):
        """Create test user and avatar"""
        self.user = User.objects.create_user(
            username='student1',
            password='testpass123',
            role='student'
        )
        self.avatar = Avatar.objects.create(
            user=self.user,
            body_color='#FF5733',
            eye_shape='round',
            mouth_shape='smile',
            accessories='glasses'
        )
    
    def test_avatar_creation(self):
        """Test that avatar is created correctly"""
        self.assertEqual(self.avatar.user, self.user)
        self.assertEqual(self.avatar.body_color, '#FF5733')
        self.assertEqual(self.avatar.eye_shape, 'round')
    
    def test_avatar_to_dict(self):
        """Test avatar to_dict method"""
        avatar_dict = self.avatar.to_dict()
        self.assertEqual(avatar_dict['body_color'], '#FF5733')
        self.assertEqual(avatar_dict['eye_shape'], 'round')
        self.assertIn('user_id', avatar_dict)
    
    def test_one_avatar_per_user(self):
        """Test that users can only have one avatar"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Avatar.objects.create(
                user=self.user,
                body_color='#00FF00'
            )


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

class AuthenticationTestCase(TestCase):
    """Test user authentication flows"""
    
    def setUp(self):
        """Create test client and users"""
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher'
        )
        self.student = User.objects.create_user(
            username='student1',
            password='testpass123',
            role='student'
        )
        self.admin = User.objects.create_user(
            username='admin1',
            password='testpass123',
            role='school_admin'
        )
    
    def test_teacher_login_redirect(self):
        """Test that teachers are redirected to teacher dashboard"""
        self.client.login(username='teacher1', password='testpass123')
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_login_redirect(self):
        """Test that students are redirected to student dashboard"""
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_login_redirect(self):
        """Test that school admins are redirected to admin dashboard"""
        self.client.login(username='admin1', password='testpass123')
        response = self.client.get(reverse('school_admin_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_required_decorator(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/accounts/login/', response.url)


# ============================================================================
# ACCESS CONTROL TESTS
# ============================================================================

class AccessControlTestCase(TestCase):
    """Test role-based access control"""
    
    def setUp(self):
        """Create test users and classes"""
        self.client = Client()
        self.teacher1 = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher',
            school='School A'
        )
        self.teacher2 = User.objects.create_user(
            username='teacher2',
            password='testpass123',
            role='teacher',
            school='School B'
        )
        self.student = User.objects.create_user(
            username='student1',
            password='testpass123',
            role='student'
        )
        self.class1 = Class.objects.create(
            name='Teacher 1 Class',
            teacher=self.teacher1,
            subject='maths',
            year_ks=2
        )
    
    def test_teacher_cannot_access_others_class(self):
        """Test that teachers cannot access other teachers' classes"""
        self.client.login(username='teacher2', password='testpass123')
        response = self.client.get(reverse('class_detail', args=[self.class1.pk]))
        # Should return 403 Forbidden or redirect
        self.assertIn(response.status_code, [403, 302])
    
    def test_student_cannot_access_teacher_dashboard(self):
        """Test that students cannot access teacher dashboard"""
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('teacher_dashboard'))
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
    
    def test_teacher_can_access_own_class(self):
        """Test that teachers can access their own classes"""
        self.client.login(username='teacher1', password='testpass123')
        response = self.client.get(reverse('class_detail', args=[self.class1.pk]))
        self.assertEqual(response.status_code, 200)


# ============================================================================
# VIEW TESTS (CRUD Operations)
# ============================================================================

class ClassCRUDTestCase(TestCase):
    """Test CRUD operations for Class model"""
    
    def setUp(self):
        """Create test teacher"""
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher'
        )
        self.client.login(username='teacher1', password='testpass123')
    
    def test_create_class(self):
        """Test creating a new class"""
        data = {
            'name': 'New Math Class',
            'subject': 'maths',
            'year_ks': 3,
            'description': 'A new math class'
        }
        response = self.client.post(reverse('add_class'), data)
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        # Verify class was created
        self.assertTrue(Class.objects.filter(name='New Math Class').exists())
    
    def test_read_class_list(self):
        """Test viewing list of classes"""
        Class.objects.create(
            name='Test Class',
            teacher=self.teacher,
            subject='science',
            year_ks=2
        )
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Class')
    
    def test_read_class_detail(self):
        """Test viewing a single class detail"""
        class_obj = Class.objects.create(
            name='Detail Test Class',
            teacher=self.teacher,
            subject='english',
            year_ks=1
        )
        response = self.client.get(reverse('class_detail', args=[class_obj.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail Test Class')
    
    def test_delete_student_from_class(self):
        """Test removing a student from a class"""
        student = User.objects.create_user(
            username='student1',
            password='testpass123',
            role='student'
        )
        class_obj = Class.objects.create(
            name='Test Class',
            teacher=self.teacher,
            subject='maths',
            year_ks=2
        )
        enrollment = ClassStudent.objects.create(
            student=student,
            clazz=class_obj
        )
        
        # Remove student
        response = self.client.post(
            reverse('remove_student', args=[class_obj.pk, student.pk])
        )
        # Should redirect after removal
        self.assertEqual(response.status_code, 302)
        # Verify enrollment was deleted
        self.assertFalse(
            ClassStudent.objects.filter(student=student, clazz=class_obj).exists()
        )


class StudentCreationTestCase(TestCase):
    """Test student account creation by teachers"""
    
    def setUp(self):
        """Create test teacher"""
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher',
            school='Test School'
        )
        self.client.login(username='teacher1', password='testpass123')
    
    def test_create_student_account(self):
        """Test that teachers can create student accounts"""
        data = {
            'username': 'newstudent1',
            'full_name': 'New Student',
            'year_ks': 2
        }
        response = self.client.post(reverse('create_student_account'), data)
        # Should create student and redirect
        self.assertTrue(User.objects.filter(username='newstudent1').exists())
        student = User.objects.get(username='newstudent1')
        self.assertEqual(student.role, 'student')
        self.assertEqual(student.school, 'Test School')


class AnalyticsViewTestCase(TestCase):
    """Test analytics views"""
    
    def setUp(self):
        """Create test data for analytics"""
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher'
        )
        self.class1 = Class.objects.create(
            name='Math Class',
            teacher=self.teacher,
            subject='maths',
            year_ks=2
        )
        self.class2 = Class.objects.create(
            name='Science Class',
            teacher=self.teacher,
            subject='science',
            year_ks=3
        )
        self.student = User.objects.create_user(
            username='student1',
            password='testpass123',
            role='student'
        )
        ClassStudent.objects.create(student=self.student, clazz=self.class1)
        
        self.client.login(username='teacher1', password='testpass123')
    
    def test_teacher_analytics_view(self):
        """Test teacher analytics dashboard"""
        response = self.client.get(reverse('teacher_analytics'))
        self.assertEqual(response.status_code, 200)
        # Should contain total counts
        self.assertContains(response, 'Math Class')
        self.assertContains(response, 'Science Class')
    
    def test_class_analytics_view(self):
        """Test class-specific analytics"""
        response = self.client.get(reverse('class_analytics', args=[self.class1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Math Class')


class SchoolAdminViewTestCase(TestCase):
    """Test school admin views"""
    
    def setUp(self):
        """Create test school admin and data"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin1',
            password='testpass123',
            role='school_admin',
            school='Test School'
        )
        self.analytics_profile = SchoolAnalyticsProfile.objects.create(
            user=self.admin,
            school='Test School'
        )
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher',
            school='Test School'
        )
        self.class_obj = Class.objects.create(
            name='Test Class',
            teacher=self.teacher,
            subject='maths',
            year_ks=2
        )
        
        self.client.login(username='admin1', password='testpass123')
    
    def test_school_admin_dashboard(self):
        """Test school admin dashboard view"""
        response = self.client.get(reverse('school_admin_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_school_admin_staff_view(self):
        """Test school admin staff list"""
        response = self.client.get(reverse('school_admin_staff'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'teacher1')
    
    def test_school_admin_classes_view(self):
        """Test school admin classes view"""
        response = self.client.get(reverse('school_admin_classes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Class')


# ============================================================================
# FORM VALIDATION TESTS
# ============================================================================

class FormValidationTestCase(TestCase):
    """Test form validation"""
    
    def setUp(self):
        """Create test teacher"""
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher'
        )
        self.client.login(username='teacher1', password='testpass123')
    
    def test_class_form_validation_missing_fields(self):
        """Test that class form requires all required fields"""
        data = {
            'name': '',  # Empty name should fail
            'subject': 'maths',
            'year_ks': 2
        }
        response = self.client.post(reverse('add_class'), data)
        # Should not redirect (form has errors)
        self.assertEqual(response.status_code, 200)
        # Should not create class
        self.assertFalse(Class.objects.filter(subject='maths').exists())
    
    def test_class_form_validation_invalid_subject(self):
        """Test that class form validates subject choices"""
        data = {
            'name': 'Test Class',
            'subject': 'invalid_subject',
            'year_ks': 2
        }
        response = self.client.post(reverse('add_class'), data)
        # Should have validation errors
        self.assertFalse(Class.objects.filter(name='Test Class').exists())


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TeacherWorkflowIntegrationTestCase(TestCase):
    """Test complete teacher workflow"""
    
    def setUp(self):
        """Create test teacher"""
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher1',
            password='testpass123',
            role='teacher',
            school='Test School'
        )
        self.client.login(username='teacher1', password='testpass123')
    
    def test_complete_class_creation_workflow(self):
        """Test complete workflow: create class, add student, view analytics"""
        # Step 1: Create class
        class_data = {
            'name': 'Integration Test Class',
            'subject': 'maths',
            'year_ks': 2,
            'description': 'Test description'
        }
        response = self.client.post(reverse('add_class'), class_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify class exists
        class_obj = Class.objects.get(name='Integration Test Class')
        self.assertEqual(class_obj.teacher, self.teacher)
        
        # Step 2: Create student
        student_data = {
            'username': 'teststudent1',
            'full_name': 'Test Student',
            'year_ks': 2
        }
        response = self.client.post(reverse('create_student_account'), student_data)
        student = User.objects.get(username='teststudent1')
        
        # Step 3: View class detail (should show student)
        response = self.client.get(reverse('class_detail', args=[class_obj.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Step 4: View analytics
        response = self.client.get(reverse('teacher_analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration Test Class')
