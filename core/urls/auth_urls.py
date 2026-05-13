from django.urls import path
from allauth.account import views as allauth_views

from core.views.auth_views import (
    custom_logout_view,
)

urlpatterns = [
    path(
        "signup/",
        allauth_views.SignupView.as_view(
            template_name="account/signup.html"
        ),
        name="signup",
    ),

    path(
        "login/",
        allauth_views.LoginView.as_view(
            template_name="account/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        custom_logout_view,
        name="logout",
    ),
]