from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.views import LoginView, SignupView


def get_dashboard_redirect_url(user):

    role = getattr(user, "role", user)

    if role == "student":
        return reverse("student_dashboard")

    if role == "school_admin":
        return reverse("school_admin_dashboard")

    return reverse("teacher_dashboard")


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):
        role = request.POST.get("role")
        if role:
            return get_dashboard_redirect_url(role)

        if request.user.is_authenticated:
            return get_dashboard_redirect_url(request.user)

        return reverse("teacher_dashboard")

    def get_login_redirect_url(self, request):

        if request.user.is_authenticated:
            return get_dashboard_redirect_url(request.user)

        return reverse("teacher_dashboard")


class FlashMessageLoginView(LoginView):

    def get_success_url(self):

        return get_dashboard_redirect_url(self.request.user)

    def form_valid(self, form):

        messages.success(self.request, "Logged in successfully.")

        return super().form_valid(form)


class FlashMessageSignupView(SignupView):

    def get_success_url(self):
        user = getattr(self, "user", None) or self.request.user
        return get_dashboard_redirect_url(user)

    def form_valid(self, form):

        messages.success(self.request, "Registration completed successfully.")

        return super().form_valid(form)

def custom_login_view(request):

    def get_role(user):
        return getattr(user, "role", None)

    if request.user.is_authenticated:

        if get_role(request.user) == "student":
            return redirect("student_dashboard")

        if get_role(request.user) == "school_admin":
            return redirect("school_admin_dashboard")

        return redirect("teacher_dashboard")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user:

                login(request, user)

                messages.success(request, "Logged in successfully.")

                if get_role(user) == "student":
                    return redirect("student_dashboard")

                if get_role(user) == "school_admin":
                    return redirect("school_admin_dashboard")

                return redirect("teacher_dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "account/login.html", {"form": form})


def custom_logout_view(request):

    logout(request)

    messages.success(request, "Logged out successfully.")

    return redirect("home")
