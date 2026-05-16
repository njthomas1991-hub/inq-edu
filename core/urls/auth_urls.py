from django.urls import path

from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
)

from django.contrib.auth import views as auth_views

from allauth.account.views import (
    LoginView,
    SignupView,
)

from core.views.auth_views import custom_logout_view
from core.forms.auth_forms import CustomPasswordChangeForm


urlpatterns = [

    # -------------------------
    # SIGNUP
    # -------------------------

    path(
        "signup/",
        SignupView.as_view(
            template_name="core/account/signup.html"
        ),
        name="account_signup",
    ),

    # -------------------------
    # LOGIN
    # -------------------------

    path(
        "login/",
        LoginView.as_view(
            template_name="core/account/login.html"
        ),
        name="account_login",
    ),

    # -------------------------
    # LOGOUT
    # -------------------------

    path(
        "logout/",
        custom_logout_view,
        name="account_logout",
    ),

    # -------------------------
    # PASSWORD CHANGE
    # -------------------------

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

    # -------------------------
    # PASSWORD RESET
    # -------------------------

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