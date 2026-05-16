from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordChangeView
from allauth.account import views as allauth_views
from django.contrib.auth import views as auth_views


from core.views.auth_views import (
    custom_logout_view,
)
from core.forms.auth_forms import CustomPasswordChangeForm

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
            form_class=CustomPasswordChangeForm,
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

path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="core/account/password_reset.html",
        email_template_name="core/account/password_reset_email.html",
        subject_template_name="core/account/password_reset_subject.txt",
    ),
    name="password_reset",
),

path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="core/account/password_reset_done.html",
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="core/account/password_reset_confirm.html",
    ),
    name="password_reset_confirm",
),

path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="core/account/password_reset_complete.html",
    ),
    name="password_reset_complete",
),
]