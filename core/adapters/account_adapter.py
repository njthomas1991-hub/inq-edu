from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):

        user = request.user

        if user.role == 'student':
            return reverse('student_dashboard')

        if user.role == 'school_admin':
            return reverse('school_admin_dashboard')

        return reverse('teacher_dashboard')

    def get_login_redirect_url(self, request):

        user = request.user

        if user.role == 'student':
            return reverse('student_dashboard')

        if user.role == 'school_admin':
            return reverse('school_admin_dashboard')

        return reverse('teacher_dashboard')