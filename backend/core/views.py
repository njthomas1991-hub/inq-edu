from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import render, redirect
from .models import User, Class, ClassStudent
import string
import random


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('name', 'subject', 'year_ks', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'year_ks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 4}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }, Class, ClassStudent
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


class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class StudentSignUpWithDetailsForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))


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


def student_signup_view(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "student"
            user.save()
            login(request, user)
            return redirect("student_dashboard")
    else:
        form = StudentSignUpForm()

    return render(request, "core/student_signup.html", {"form": form})


def generate_simple_password():
    """Generate a simple password for 7-9 year olds (memorable and easy)"""
    adjectives = ['Happy', 'Sunny', 'Quick', 'Brave', 'Smart', 'Cool', 'Bright', 'Clever']
    nouns = ['Bear', 'Lion', 'Tiger', 'Eagle', 'Panda', 'Fox', 'Wolf', 'Hawk']
    number = random.randint(1, 9)
    return f"{random.choice(adjectives)}{random.choice(nouns)}{number}"


def student_signup_with_details_view(request):
    if request.method == "POST":
        form = StudentSignUpWithDetailsForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            # Auto-generate username: firstname + last name initial
            username = (first_name + last_name[0]).lower()
            
            # Check if username already exists, if so add a number
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            # Auto-generate simple password
            password = generate_simple_password()
            
            return render(request, "core/student_signup_confirmation.html", {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "password": password,
            })
    else:
        form = StudentSignUpWithDetailsForm()

    return render(request, "core/student_signup_with_details.html", {"form": form})


def create_student_account_view(request):
    """API endpoint to create student account from confirmation page"""
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if username and password:
            # Create the student user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='student'
            )
            return render(request, "core/student_account_created.html", {
                "username": username,
                "password": password,
            })
    
    return redirect("student_signup_guided")


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


@login_required
def class_detail_view(request, class_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    class_obj = Class.objects.get(id=class_id)
    if class_obj.teacher_id != request.user.id:
        return HttpResponseForbidden("You don't have access to this class")

    students = class_obj.students.all().select_related('student')

    return render(request, "core/class_detail.html", {
        "class_obj": class_obj,
        "students": students,
    })


@login_required
def add_class_view(request):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            class_obj = form.save(commit=False)
            class_obj.teacher = request.user
            class_obj.save()
            return redirect("teacher_dashboard")
    else:
        form = ClassForm()

    return render(request, "core/add_class.html", {"form": form})


