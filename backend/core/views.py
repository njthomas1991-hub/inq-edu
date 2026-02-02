from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import render, redirect
from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Simple home page view
def home_page_view(request):
    return HttpResponse("Welcome to inq-ed! Your inquiry-based education platform is live.")

@api_view(['GET'])
def hello(request):
    return Response({"message": "Hello from Django API!"})


class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    school = forms.CharField(required=False, max_length=255)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "school", "password1", "password2")


def teacher_signup_view(request):
    if request.method == "POST":
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "teacher"
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect("teacher_dashboard")
    else:
        form = TeacherSignUpForm()

    return render(request, "core/teacher_signup.html", {"form": form})


@login_required
def teacher_dashboard_view(request):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    classes = request.user.classes_taught.all()
    analytics_profile = getattr(request.user, "analytics_profile", None)

    return render(request, "core/teacher_dashboard.html", {
        "classes": classes,
        "analytics_profile": analytics_profile,
    })


