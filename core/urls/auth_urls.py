from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordChangeView
from allauth.account import views as allauth_views

from core.views.auth_views import (
    custom_logout_view,
)

urlpatterns = [
    path(
        "signup/",
        allauth_views.SignupView.as_view(
            template_name="accounts/signup.html"
        ),
        name="signup",
    ),

    path(
        "login/",
        allauth_views.LoginView.as_view(
            template_name="accounts/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        custom_logout_view,
        name="logout",
    ),

    path(
        "password/change/",
        PasswordChangeView.as_view(
            template_name="core/account/password_change.html"
        ),
        name="password_change"
    ),

    path(
        "password/change/done/",
        PasswordChangeDoneView.as_view(
            template_name="core/account/password_change_done.html"
        ),
        name="password_change_done"
    ),
]