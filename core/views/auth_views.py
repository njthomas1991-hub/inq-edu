from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


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
        "core/accounts/login.html",
        {
            "form": form
        }
    )


def custom_logout_view(request):

    logout(request)

    return redirect("home")