from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):

        user = request.user

        if user.is_authenticated:

            if getattr(user, "role", None) == "student":
                return reverse("student_dashboard")

            if getattr(user, "role", None) == "school_admin":
                return reverse("school_admin_dashboard")

        return reverse("teacher_dashboard")

    def get_login_redirect_url(self, request):

        user = request.user

        if user.is_authenticated:

            if getattr(user, "role", None) == "student":
                return reverse("student_dashboard")

            if getattr(user, "role", None) == "school_admin":
                return reverse("school_admin_dashboard")

        return reverse("teacher_dashboard")

def custom_login_view(request):

    def get_role(user):
        return getattr(user, "role", None)

    if request.user.is_authenticated:

        if get_role(request.user) == "student":
            return redirect("student_dashboard")

        if get_role(request.user) == "school_admin":
            return redirect("school_admin_dashboard")

        return redirect("teacher_dashboard")

    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:

                login(request, user)

                if get_role(user) == "student":
                    return redirect("student_dashboard")

                if get_role(user) == "school_admin":
                    return redirect("school_admin_dashboard")

                return redirect("teacher_dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


def custom_logout_view(request):

    logout(request)

    return redirect("home")