from django.urls import path
from allauth.account import views as allauth_views

from core.views.auth_views import (
    custom_logout_view,
)

urlpatterns = [
    path(
        "teacher/signup/",
        allauth_views.SignupView.as_view(
            template_name="core/auth/teacher_signup.html"
        ),
        name="signup",
    ),

    path(
        "teacher/login/",
        allauth_views.LoginView.as_view(
            template_name="core/auth/teacher_login.html"
        ),
        name="teacher_login",
    ),

    path(
        "logout/",
        custom_logout_view,
        name="logout",
    ),
]