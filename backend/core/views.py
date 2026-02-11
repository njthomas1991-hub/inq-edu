from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django_summernote.widgets import SummernoteWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from .models import (
    User, Class, ClassStudent,
    NewsAnnouncement, HelpTutorial, TeachingResource,
    ForumPost, ForumReply, ResourceComment, Avatar
)

import string
import random
import json


class CustomSignupForm(SignupForm):
    """Custom signup form with role selection"""
    ROLE_DESCRIPTIONS = {
        'teacher': 'A teacher who creates and manages classes and students.',
        'student': 'A student who participates in classes and activities.',
        'school_admin': 'This role is for the person who manages the school\'s information. As a School Admin, you can view and track teachers, classes, and students linked to your school. Choose this role if you need full oversight of your school\'s data.',
    }
    
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'role-radio'}),
        required=True,
        label='I am a',
        initial='teacher'
    )
    first_name = forms.CharField(max_length=150, required=False, label='First Name')
    last_name = forms.CharField(max_length=150, required=False, label='Last Name')
    school = forms.CharField(max_length=255, required=False, label='School')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add role descriptions to help text
        self.fields['role'].help_text = 'Select your role'
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.role = self.cleaned_data['role']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.school = self.cleaned_data.get('school', '')
        user.is_staff = user.role in ['teacher', 'school_admin']
        user.save()
        return user


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter to redirect based on user role"""
    def get_signup_redirect_url(self, request):
        user = request.user
        if user.is_authenticated:
            if user.role == 'student':
                return '/student/'
            elif user.role == 'school_admin':
                return '/school-admin/'
        return '/teacher/'

    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_authenticated:
            if getattr(user, "role", None) == "student":
                return reverse("student_dashboard")
            if getattr(user, "role", None) == "school_admin":
                return reverse("school_admin_dashboard")
        return reverse("teacher_dashboard")


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('name', 'year_ks', 'subject', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class name'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'year_ks': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }


class TeachingResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-6'),
                Column('resource_type', css_class='col-md-6'),
                css_class='g-3'
            ),
            Row(
                Column('key_stage', css_class='col-md-6'),
                Column('subject', css_class='col-md-6'),
                css_class='g-3'
            ),
            Row(
                Column('excerpt', css_class='col-12'),
                css_class='g-3'
            ),
            Row(
                Column('image', css_class='col-md-6'),
                Column('file', css_class='col-md-6'),
                css_class='g-3'
            ),
            Row(
                Column('content', css_class='col-12'),
                css_class='g-3'
            ),
            Row(
                Column('status', css_class='col-md-4'),
                css_class='g-3'
            ),
        )

    class Meta:
        model = TeachingResource
        fields = ('title', 'content', 'excerpt', 'image', 'file', 'resource_type', 'key_stage', 'subject', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource title'}),
            'content': SummernoteWidget(attrs={'summernote': {'height': '400'}}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Short summary'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx'}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'key_stage': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 4}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject (optional)'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ('title', 'image', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Discussion title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(attrs={'summernote': {'height': '300'}}),
        }


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ('content',)
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'height': '250'}}),
        }


class ResourceCommentForm(forms.ModelForm):
    class Meta:
        model = ResourceComment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your thoughts on this resource...'}),
        }

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Simple home page view
def home_page_view(request):
    return render(request, "core/home.html")


def about_page_view(request):
    return render(request, "core/about.html")


def kindlewick_page_view(request):
    return render(request, "core/kindlewick.html")


def questopia_page_view(request):
    return render(request, "core/questopia.html")


def pricing_page_view(request):
    return render(request, "core/pricing.html")


def teacher_hub_view(request):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")
    return render(request, "core/teacher_hub.html")


def contact_page_view(request):
    return render(request, "core/contact.html")


def wonderworld_page_view(request):
    return render(request, "core/wonderworld.html")


@login_required
def student_dashboard_view(request):
    if getattr(request.user, "role", None) != "student":
        return HttpResponseForbidden("Student access only")

    enrollments = ClassStudent.objects.filter(student=request.user).select_related('clazz')
    total_classes = enrollments.count()
    
    # Get unique key stages from enrolled classes and define available worlds
    key_stages = enrollments.values_list('clazz__year_ks', flat=True).distinct().order_by('clazz__year_ks')
    
    # Map key stages to game worlds
    worlds = [
        {'ks': 0, 'label': 'EYFS', 'name': 'Moonbeam Meadows', 'status': 'coming_soon', 'url': ''},
        {'ks': 1, 'label': 'KS1', 'name': 'Starlit Shores', 'status': 'coming_soon', 'url': ''},
        {'ks': 2, 'label': 'Lower KS2', 'name': 'Kindle Wick', 'status': 'available', 'url': 'kindlewick'},
        {'ks': 3, 'label': 'Upper KS2', 'name': 'Questopia', 'status': 'coming_soon', 'url': ''},
        {'ks': 4, 'label': 'KS3', 'name': 'WonderWorld', 'status': 'coming_soon', 'url': ''},
        {'ks': 5, 'label': 'KS4', 'name': 'Nexus Trials', 'status': 'coming_soon', 'url': ''},
    ]
    
    # Filter worlds to only those the student has classes for
    available_worlds = [w for w in worlds if w['ks'] in key_stages]

    return render(request, "core/student_dashboard.html", {
        "enrollments": enrollments,
        "total_classes": total_classes,
        "available_worlds": available_worlds,
    })

@api_view(['GET'])
def hello(request):
    return Response({"message": "Hello from Django API!"})


def custom_login_view(request):
    """Custom login that redirects based on user role"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on role
                if user.role == 'student':
                    return redirect('student_dashboard')
                elif user.role == 'school_admin':
                    return redirect('admin:index')
                else:  # teacher
                    return redirect('teacher_dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, "core/teacher_login.html", {"form": form})


class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    school = forms.CharField(required=False, max_length=255)
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "school", "role", "password1", "password2")


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
            user.role = form.cleaned_data.get("role", "teacher")
            user.is_staff = user.role == "teacher"
            user.save()
            login(request, user)
            if user.role == "student":
                return redirect("student_dashboard")
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
    class_id = request.GET.get('class_id') or request.POST.get('class_id')
    
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
                "class_id": class_id,
            })
    else:
        form = StudentSignUpWithDetailsForm()

    return render(request, "core/student_signup_with_details.html", {
        "form": form,
        "class_id": class_id,
    })


def create_student_account_view(request):
    """API endpoint to create student account from confirmation page"""
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        class_id = request.POST.get('class_id', '')
        
        if username and password:
            # Create the student user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='student',
                plain_password=password  # Store plain password for display
            )
            
            # If class_id is provided, enroll student in class
            if class_id:
                try:
                    class_obj = Class.objects.get(id=class_id)
                    ClassStudent.objects.create(student=user, clazz=class_obj)
                    messages.success(request, f'Student account "{username}" created and added to class successfully!')
                    # Redirect back to class detail page
                    return redirect('class_detail', class_id=class_id)
                except Class.DoesNotExist:
                    pass
            
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
def teacher_analytics_view(request):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    classes = request.user.classes_taught.all().prefetch_related("students")
    total_students = sum(clazz.students.count() for clazz in classes)

    subject_counts = {}
    key_stage_counts = {}
    for clazz in classes:
        subject_label = clazz.get_subject_display()
        subject_counts[subject_label] = subject_counts.get(subject_label, 0) + 1
        key_stage_label = clazz.key_stage_label
        key_stage_counts[key_stage_label] = key_stage_counts.get(key_stage_label, 0) + 1

    subject_breakdown = [
        {"label": label, "count": count} for label, count in subject_counts.items()
    ]
    key_stage_breakdown = [
        {"label": label, "count": count} for label, count in key_stage_counts.items()
    ]

    return render(request, "core/teacher_analytics.html", {
        "classes": classes,
        "classes_count": classes.count(),
        "total_students": total_students,
        "subject_breakdown": subject_breakdown,
        "key_stage_breakdown": key_stage_breakdown,
    })


@login_required
def class_detail_view(request, class_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    class_obj = Class.objects.get(id=class_id)
    if class_obj.teacher_id != request.user.id:
        return HttpResponseForbidden("You don't have access to this class")

    students = class_obj.students.all().select_related('student').order_by('student__first_name', 'student__last_name')
    teacher_classes = Class.objects.filter(teacher=request.user)

    return render(request, "core/class_detail.html", {
        "class_obj": class_obj,
        "students": students,
        "teacher_classes": teacher_classes,
    })


@login_required
def class_analytics_view(request, class_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    class_obj = get_object_or_404(Class, id=class_id)
    if class_obj.teacher_id != request.user.id:
        return HttpResponseForbidden("You don't have access to this class")

    enrollments = ClassStudent.objects.filter(clazz=class_obj).select_related("student")
    total_students = enrollments.count()

    return render(request, "core/class_analytics.html", {
        "class_obj": class_obj,
        "students": enrollments,
        "total_students": total_students,
    })


@login_required
def student_analytics_view(request, class_id, student_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    class_obj = get_object_or_404(Class, id=class_id)
    if class_obj.teacher_id != request.user.id:
        return HttpResponseForbidden("You don't have access to this class")

    enrollment = get_object_or_404(ClassStudent, clazz=class_obj, student_id=student_id)
    student = enrollment.student

    return render(request, "core/student_analytics.html", {
        "class_obj": class_obj,
        "student": student,
        "enrollment": enrollment,
    })


@login_required
def remove_student_view(request, class_id, student_id):
    """Remove a student from a class"""
    if request.method != "POST":
        return HttpResponseForbidden("POST method required")
    
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    try:
        class_obj = Class.objects.get(id=class_id)
        if class_obj.teacher_id != request.user.id:
            return HttpResponseForbidden("You don't have access to this class")
        
        # Remove the student from the class
        student = get_object_or_404(User, id=student_id)
        ClassStudent.objects.filter(clazz=class_obj, student_id=student_id).delete()
        messages.success(request, f'Student "{student.get_full_name() or student.username}" removed from class successfully.')
        
    except Class.DoesNotExist:
        messages.error(request, 'Class not found.')
        return HttpResponseForbidden("Class not found")
    
    return redirect('class_detail', class_id=class_id)


@login_required
def transfer_student_view(request, class_id, student_id):
    """Transfer a student from one class to another"""
    if request.method != "POST":
        return HttpResponseForbidden("POST method required")
    
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    try:
        source_class = Class.objects.get(id=class_id)
        if source_class.teacher_id != request.user.id:
            return HttpResponseForbidden("You don't have access to this class")
        
        target_class_id = request.POST.get('target_class_id')
        target_class = Class.objects.get(id=target_class_id)
        
        # Verify teacher owns target class too
        if target_class.teacher_id != request.user.id:
            return HttpResponseForbidden("You don't have access to the target class")
        
        # Get the enrollment
        enrollment = ClassStudent.objects.get(clazz=source_class, student_id=student_id)
        
        # Check if student is already in target class
        if not ClassStudent.objects.filter(clazz=target_class, student_id=student_id).exists():
            # Update the enrollment to point to new class
            enrollment.clazz = target_class
            enrollment.save()
        else:
            # Student already in target class, just remove from source
            enrollment.delete()
        
    except (Class.DoesNotExist, ClassStudent.DoesNotExist):
        return HttpResponseForbidden("Class or enrollment not found")
    
    return redirect('class_detail', class_id=class_id)


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
            messages.success(request, f'Class "{class_obj.name}" created successfully!')
            return redirect("teacher_dashboard")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClassForm()

    return render(request, "core/add_class.html", {"form": form})


@login_required
def teacher_news_list_view(request):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    if request.user.is_superuser:
        news_items = NewsAnnouncement.objects.all()
    else:
        news_items = NewsAnnouncement.objects.filter(status='published')

    paginator = Paginator(news_items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    return render(request, "core/teacher_news_list.html", {
        "news_items": page_obj,
        "page_obj": page_obj,
        "is_paginated": is_paginated,
    })


@login_required
def teacher_news_detail_view(request, slug):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    if request.user.is_superuser:
        news_item = get_object_or_404(NewsAnnouncement, slug=slug)
    else:
        news_item = get_object_or_404(NewsAnnouncement, slug=slug, status='published')

    return render(request, "core/teacher_news_detail.html", {
        "news_item": news_item,
    })


@login_required
def teacher_help_list_view(request):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    if request.user.is_superuser:
        tutorials = HelpTutorial.objects.all()
    else:
        tutorials = HelpTutorial.objects.filter(status='published')

    paginator = Paginator(tutorials, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    return render(request, "core/teacher_help_list.html", {
        "tutorials": page_obj,
        "page_obj": page_obj,
        "is_paginated": is_paginated,
    })


@login_required
def teacher_help_detail_view(request, slug):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    if request.user.is_superuser:
        tutorial = get_object_or_404(HelpTutorial, slug=slug)
    else:
        tutorial = get_object_or_404(HelpTutorial, slug=slug, status='published')

    return render(request, "core/teacher_help_detail.html", {
        "tutorial": tutorial,
    })


@login_required
def teacher_resources_list_view(request):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    resources = TeachingResource.objects.filter(
        Q(status='published') | Q(author=request.user)
    ).distinct()

    if request.method == "POST":
        form = TeachingResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = request.user
            resource.save()
            form.save_m2m()
            messages.success(request, f'Resource "{resource.title}" created successfully!')
            return redirect("teacher_resources")
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = TeachingResourceForm()

    paginator = Paginator(resources, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    return render(request, "core/teacher_resources_list.html", {
        "resources": page_obj,
        "page_obj": page_obj,
        "is_paginated": is_paginated,
        "form": form,
    })


@login_required
def teacher_resource_detail_view(request, slug):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    resource = get_object_or_404(
        TeachingResource,
        slug=slug,
    )

    if resource.status != 'published' and resource.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have access to this resource")

    if request.method == "POST":
        comment_form = ResourceCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.resource = resource
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect("teacher_resource_detail", slug=resource.slug)
    else:
        comment_form = ResourceCommentForm()

    return render(request, "core/teacher_resource_detail.html", {
        "resource": resource,
        "comment_form": comment_form,
    })


@login_required
def teacher_resource_edit_view(request, slug):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    resource = get_object_or_404(TeachingResource, slug=slug)

    if resource.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only edit your own resources")

    if request.method == "POST":
        form = TeachingResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, f'Resource "{resource.title}" updated successfully.')
            return redirect("teacher_resource_detail", slug=resource.slug)
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = TeachingResourceForm(instance=resource)

    return render(request, "core/teacher_resource_edit.html", {
        "resource": resource,
        "form": form,
    })


@login_required
def teacher_resource_delete_view(request, slug):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    resource = get_object_or_404(TeachingResource, slug=slug)

    if resource.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only delete your own resources")

    if request.method == "POST":
        resource_title = resource.title
        resource.delete()
        messages.success(request, f'Resource "{resource_title}" deleted successfully.')
        return redirect("teacher_resources")

    return redirect("teacher_resource_detail", slug=slug)


@login_required
def teacher_resource_comment_delete_view(request, slug, comment_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    resource = get_object_or_404(TeachingResource, slug=slug)
    comment = get_object_or_404(ResourceComment, id=comment_id, resource=resource)

    if comment.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only delete your own comments")

    if request.method == "POST":
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect("teacher_resource_detail", slug=resource.slug)

    return redirect("teacher_resource_detail", slug=resource.slug)


@login_required
def teacher_forum_list_view(request):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    posts = ForumPost.objects.all()

    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'Discussion "{post.title}" created successfully!')
            return redirect("teacher_forum")
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ForumPostForm()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    return render(request, "core/teacher_forum_list.html", {
        "posts": page_obj,
        "page_obj": page_obj,
        "is_paginated": is_paginated,
        "form": form,
    })


@login_required
@login_required
def profile_view(request):
    user = request.user
    role = getattr(user, "role", None)
    activity_log = []

    if request.method == "POST":
        action = request.POST.get("bio_action")
        if action == "save":
            bio = (request.POST.get("bio") or "").strip()
            user.bio = bio if bio else None
            user.save(update_fields=["bio"])
        elif action == "clear":
            user.bio = None
            user.save(update_fields=["bio"])

        return redirect("profile")

    def add_activity(message, timestamp):
        if timestamp:
            activity_log.append({
                "message": message,
                "timestamp": timestamp,
            })

    if role == "teacher":
        classes_taught = user.classes_taught.all()
        template_name = "core/teacher_profile.html"

        for clazz in classes_taught.order_by("-created_at")[:6]:
            add_activity(f"Created class {clazz.name}", clazz.created_at)

        for resource in TeachingResource.objects.filter(author=user).order_by("-created_at")[:6]:
            add_activity(f"Published resource {resource.title}", resource.created_at)

        for post in ForumPost.objects.filter(author=user).order_by("-created_at")[:6]:
            add_activity(f"Posted to forum {post.title}", post.created_at)

        for announcement in NewsAnnouncement.objects.filter(author=user).order_by("-created_at")[:6]:
            add_activity(f"Shared announcement {announcement.title}", announcement.created_at)

        context = {
            "classes_taught": classes_taught,
            "classes_count": classes_taught.count(),
        }
    else:
        enrollments = user.enrolled_classes.select_related("clazz").all()
        template_name = "core/student_profile.html"

        for enrollment in enrollments.order_by("-date_joined")[:8]:
            add_activity(f"Joined class {enrollment.clazz.name}", enrollment.date_joined)

        context = {
            "enrollments": enrollments,
            "classes_count": enrollments.count(),
        }

    activity_log = sorted(activity_log, key=lambda item: item["timestamp"], reverse=True)
    activity_log = activity_log[:8]

    context.update({
        "profile_user": user,
        "avatar": getattr(user, 'avatar', None),
        "activity_log": activity_log,
    })

    return render(request, template_name, context)


@login_required
def account_settings_view(request):
    user = request.user
    role = getattr(user, "role", None)

    if role == "teacher":
        template_name = "core/account_settings_teacher.html"
    else:
        template_name = "core/account_settings_student.html"

    return render(request, template_name, {
        "profile_user": user,
    })


@login_required
def teacher_forum_detail_view(request, post_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    post = get_object_or_404(ForumPost, id=post_id)

    if request.method == "POST":
        if post.is_locked:
            return HttpResponseForbidden("This thread is locked")
        reply_form = ForumReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.author = request.user
            reply.post = post
            reply.save()
            return redirect("teacher_forum_detail", post_id=post.id)
    else:
        reply_form = ForumReplyForm()
        ForumPost.objects.filter(id=post_id).update(views=F('views') + 1)

    return render(request, "core/teacher_forum_detail.html", {
        "post": post,
        "reply_form": reply_form,
    })


@login_required
def teacher_forum_edit_view(request, post_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    post = get_object_or_404(ForumPost, id=post_id)

    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only edit your own discussions")

    if request.method == "POST":
        form = ForumPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f'Discussion "{post.title}" updated successfully.')
            return redirect("teacher_forum_detail", post_id=post.id)
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ForumPostForm(instance=post)

    return render(request, "core/teacher_forum_edit.html", {
        "post": post,
        "form": form,
    })


@login_required
def teacher_forum_delete_view(request, post_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    post = get_object_or_404(ForumPost, id=post_id)

    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only delete your own discussions")

    if request.method == "POST":
        post_title = post.title
        post.delete()
        messages.success(request, f'Discussion "{post_title}" deleted successfully.')
        return redirect("teacher_forum")

    return redirect("teacher_forum_detail", post_id=post.id)


@login_required
def teacher_forum_reply_edit_view(request, post_id, reply_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    post = get_object_or_404(ForumPost, id=post_id)
    reply = get_object_or_404(ForumReply, id=reply_id, post=post)

    if reply.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only edit your own replies")

    if request.method == "POST":
        form = ForumReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            return redirect("teacher_forum_detail", post_id=post.id)
    else:
        form = ForumReplyForm(instance=reply)

    return render(request, "core/teacher_forum_reply_edit.html", {
        "post": post,
        "reply": reply,
        "form": form,
    })


@login_required
def teacher_forum_reply_delete_view(request, post_id, reply_id):
    if getattr(request.user, "role", None) != "teacher":
        return HttpResponseForbidden("Teacher access only")

    post = get_object_or_404(ForumPost, id=post_id)
    reply = get_object_or_404(ForumReply, id=reply_id, post=post)

    if reply.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only delete your own replies")

    if request.method == "POST":
        reply.delete()
        return redirect("teacher_forum_detail", post_id=post.id)

    return redirect("teacher_forum_detail", post_id=post.id)


# ============== AVATAR API VIEWS ==============

@login_required
@require_http_methods(["GET"])
def get_user_avatar(request):
    """
    Get user's avatar data as JSON.
    
    Returns the avatar traits or creates a default avatar if none exists.
    """
    try:
        avatar, created = Avatar.objects.get_or_create(
            user=request.user,
            defaults={
                'body_type': 'blob',
                'body_color': '#FF6B9D',
                'eye_type': 'big_round',
                'mouth_type': 'happy',
                'head_decoration': 'horns',
                'decoration_color': '#FFB347',
                'pattern': 'solid',
                'pattern_color': '#FF1493'
            }
        )
        
        # Ensure all fields have values (for old records)
        avatar_dict = avatar.to_dict()
        avatar_dict.setdefault('bodyColor', '#FF6B9D')
        avatar_dict.setdefault('decorationColor', '#FFB347')
        avatar_dict.setdefault('patternColor', '#FF1493')
        avatar_dict.setdefault('pattern', 'solid')
        avatar_dict.setdefault('headDecoration', 'horns')
        
        return JsonResponse(avatar_dict)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def save_user_avatar(request):
    """
    Save user's avatar traits.
    
    Request body (JSON) - accepts both camelCase and snake_case:
        {
            'bodyType': 'round_blue',  OR  'body_type': 'round_blue'
            'eyeType': 'big_happy',    OR  'eye_type': 'big_happy'
            ...
        }
    
    Returns:
        {'success': True, 'avatar': {...}}
    """
    try:
        data = json.loads(request.body)
        
        avatar, created = Avatar.objects.get_or_create(user=request.user)
        
        # Update avatar traits - accept both camelCase and snake_case
        avatar.body_type = data.get('body_type') or data.get('bodyType', avatar.body_type)
        avatar.body_color = data.get('body_color') or data.get('bodyColor', avatar.body_color)
        avatar.eye_type = data.get('eye_type') or data.get('eyeType', avatar.eye_type)
        avatar.mouth_type = data.get('mouth_type') or data.get('mouthType', avatar.mouth_type)
        avatar.head_decoration = data.get('head_decoration') or data.get('headDecoration', avatar.head_decoration)
        avatar.decoration_color = data.get('decoration_color') or data.get('decorationColor', avatar.decoration_color)
        avatar.pattern = data.get('pattern', avatar.pattern)
        avatar.pattern_color = data.get('pattern_color') or data.get('patternColor', avatar.pattern_color)
        
        avatar.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Avatar saved successfully',
            'avatar': avatar.to_dict()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def randomize_avatar(request):
    """
    Randomize user's avatar with random traits.
    
    Returns:
        {'success': True, 'avatar': {...}}
    """
    try:
        import random as rand
        
        avatar, created = Avatar.objects.get_or_create(user=request.user)
        
        body_choices = [choice[0] for choice in Avatar.BODY_TYPES]
        eye_choices = [choice[0] for choice in Avatar.EYE_TYPES]
        mouth_choices = [choice[0] for choice in Avatar.MOUTH_TYPES]
        decoration_choices = [choice[0] for choice in Avatar.DECORATION_TYPES]
        pattern_choices = [choice[0] for choice in Avatar.PATTERN_TYPES]
        
        colors = ['#FF6B9D', '#FFB347', '#FF1493', '#FF69B4', '#87CEFA', 
                  '#98D8C8', '#F7DC6F', '#BB8FCE', '#F8B88B', '#95E1D3']
        
        avatar.body_type = rand.choice(body_choices)
        avatar.body_color = rand.choice(colors)
        avatar.eye_type = rand.choice(eye_choices)
        avatar.mouth_type = rand.choice(mouth_choices)
        avatar.head_decoration = rand.choice(decoration_choices)
        avatar.decoration_color = rand.choice(colors)
        avatar.pattern = rand.choice(pattern_choices)
        avatar.pattern_color = rand.choice(colors)
        
        avatar.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Avatar randomized',
            'avatar': avatar.to_dict()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ==================== SCHOOL ADMIN VIEWS ====================

@login_required
def school_admin_dashboard_view(request):
    """School admin dashboard showing overview of staff, classes, and students"""
    if getattr(request.user, "role", None) != "school_admin":
        return HttpResponseForbidden("School admin access only")
    
    if not request.user.school:
        return HttpResponseForbidden("You are not associated with a school")
    
    # Get all teachers in the same school
    teachers = User.objects.filter(role='teacher', school=request.user.school).order_by('first_name', 'last_name')
    
    # Get all classes taught by teachers in this school
    classes = Class.objects.filter(teacher__school=request.user.school).select_related('teacher').order_by('-created_at')
    
    # Get total students across all classes
    total_students = ClassStudent.objects.filter(clazz__teacher__school=request.user.school).values('student').distinct().count()
    
    # Recent activity (last 10 classes created)
    recent_classes = classes[:10]
    
    context = {
        'teachers_count': teachers.count(),
        'classes_count': classes.count(),
        'total_students': total_students,
        'recent_classes': recent_classes,
    }
    
    return render(request, "core/school_admin_dashboard.html", context)


@login_required
def school_admin_staff_view(request):
    """List all teachers registered to the same school"""
    if getattr(request.user, "role", None) != "school_admin":
        return HttpResponseForbidden("School admin access only")
    
    if not request.user.school:
        return HttpResponseForbidden("You are not associated with a school")
    
    # Get all teachers in the same school
    teachers = User.objects.filter(
        role='teacher', 
        school=request.user.school
    ).prefetch_related('classes_taught').order_by('first_name', 'last_name')
    
    # Add class count for each teacher
    for teacher in teachers:
        teacher.class_count = teacher.classes_taught.count()
    
    context = {
        'teachers': teachers,
        'school_name': request.user.school,
    }
    
    return render(request, "core/school_admin_staff.html", context)


@login_required
def school_admin_classes_view(request):
    """List all classes with links to teachers"""
    if getattr(request.user, "role", None) != "school_admin":
        return HttpResponseForbidden("School admin access only")
    
    if not request.user.school:
        return HttpResponseForbidden("You are not associated with a school")
    
    # Get all classes taught by teachers in this school
    classes = Class.objects.filter(
        teacher__school=request.user.school
    ).select_related('teacher').prefetch_related('students').order_by('-created_at')
    
    # Add student count for each class
    for clazz in classes:
        clazz.student_count = clazz.students.count()
    
    context = {
        'classes': classes,
        'school_name': request.user.school,
    }
    
    return render(request, "core/school_admin_classes.html", context)


@login_required
def school_admin_analytics_view(request):
    """School-wide analytics dashboard"""
    if getattr(request.user, "role", None) != "school_admin":
        return HttpResponseForbidden("School admin access only")
    
    if not request.user.school:
        return HttpResponseForbidden("You are not associated with a school")
    
    # Get all classes in this school
    classes = Class.objects.filter(teacher__school=request.user.school).select_related('teacher')
    
    # Analytics by subject
    subject_counts = {}
    key_stage_counts = {}
    
    for clazz in classes:
        subject_label = clazz.get_subject_display()
        subject_counts[subject_label] = subject_counts.get(subject_label, 0) + 1
        key_stage_label = clazz.key_stage_label
        key_stage_counts[key_stage_label] = key_stage_counts.get(key_stage_label, 0) + 1
    
    subject_breakdown = [
        {"label": label, "count": count} for label, count in subject_counts.items()
    ]
    key_stage_breakdown = [
        {"label": label, "count": count} for label, count in key_stage_counts.items()
    ]
    
    # Total students
    total_students = ClassStudent.objects.filter(clazz__teacher__school=request.user.school).values('student').distinct().count()
    
    context = {
        'classes': classes,
        'classes_count': classes.count(),
        'total_students': total_students,
        'subject_breakdown': subject_breakdown,
        'key_stage_breakdown': key_stage_breakdown,
        'school_name': request.user.school,
    }
    
    return render(request, "core/school_admin_analytics.html", context)


@login_required
def school_admin_activity_log_view(request):
    """Activity log showing recent classes created and students joined"""
    if getattr(request.user, "role", None) != "school_admin":
        return HttpResponseForbidden("School admin access only")
    
    if not request.user.school:
        return HttpResponseForbidden("You are not associated with a school")
    
    # Get recent classes created
    recent_classes = Class.objects.filter(
        teacher__school=request.user.school
    ).select_related('teacher').order_by('-created_at')[:20]
    
    # Get recent student enrollments
    recent_enrollments = ClassStudent.objects.filter(
        clazz__teacher__school=request.user.school
    ).select_related('student', 'clazz', 'clazz__teacher').order_by('-date_joined')[:20]
    
    # Combine into chronological activity log
    activity_log = []
    
    for clazz in recent_classes:
        activity_log.append({
            'type': 'class_created',
            'timestamp': clazz.created_at,
            'class': clazz,
            'teacher': clazz.teacher,
        })
    
    for enrollment in recent_enrollments:
        activity_log.append({
            'type': 'student_joined',
            'timestamp': enrollment.date_joined,
            'student': enrollment.student,
            'class': enrollment.clazz,
            'teacher': enrollment.clazz.teacher,
        })
    
    # Sort by timestamp descending
    activity_log.sort(key=lambda x: x['timestamp'], reverse=True)
    activity_log = activity_log[:30]  # Limit to 30 most recent activities
    
    context = {
        'activity_log': activity_log,
        'school_name': request.user.school,
    }
    
    return render(request, "core/school_admin_activity_log.html", context)


# Kindlewick API Endpoints
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer, AvatarSerializer, KindlewickGameProgressSerializer, 
    KindlewickGameSessionSerializer, KindlewickGameProgressAdminSerializer,
    KindlewickGameSessionAdminSerializer
)
from .models import KindlewickGameProgress, KindlewickGameSession, User
from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_api(request):
    """Get current logged-in user info"""
    user = request.user
    avatar = getattr(user, 'avatar', None)
    
    user_data = UserSerializer(user).data
    user_data['avatar'] = AvatarSerializer(avatar).data if avatar else None
    
    return Response(user_data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def kindlewick_progress_list(request):
    """Get or update Kindlewick game progress for current user"""
    if request.method == 'GET':
        # Get all progress for current student
        if request.user.role != 'student':
            return Response({'error': 'Only students can access their progress'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        progress = KindlewickGameProgress.objects.filter(user=request.user)
        serializer = KindlewickGameProgressSerializer(progress, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create or update progress
        if request.user.role != 'student':
            return Response({'error': 'Only students can update progress'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        game_type = request.data.get('game_type')
        
        # Get or create progress record
        progress, created = KindlewickGameProgress.objects.get_or_create(
            user=request.user,
            game_type=game_type
        )
        
        # Update fields from request
        if 'current_level' in request.data:
            progress.current_level = request.data['current_level']
        if 'score' in request.data:
            progress.score = request.data['score']
        if 'tokens_earned' in request.data:
            progress.tokens_earned = request.data['tokens_earned']
        if 'total_playtime' in request.data:
            progress.total_playtime = request.data['total_playtime']
        if 'completed' in request.data:
            progress.completed = request.data['completed']
        
        progress.save()
        serializer = KindlewickGameProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def kindlewick_sessions(request):
    """Get game sessions or create a new session"""
    if request.method == 'GET':
        if request.user.role != 'student':
            return Response({'error': 'Only students can access their sessions'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        sessions = KindlewickGameSession.objects.filter(user=request.user).order_by('-created_at')[:50]
        serializer = KindlewickGameSessionSerializer(sessions, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if request.user.role != 'student':
            return Response({'error': 'Only students can create sessions'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        game_type = request.data.get('game_type')
        level = request.data.get('level', 1)
        
        session = KindlewickGameSession.objects.create(
            user=request.user,
            game_type=game_type,
            level=level,
            session_data=request.data.get('session_data', {})
        )
        
        serializer = KindlewickGameSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def kindlewick_session_detail(request, session_id):
    """Get, update, or finish a game session"""
    try:
        session = KindlewickGameSession.objects.get(id=session_id)
    except KindlewickGameSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check permission
    if session.user != request.user and request.user.role != 'teacher':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = KindlewickGameSessionSerializer(session)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Update session data
        if 'score' in request.data:
            session.score = request.data['score']
        if 'tokens_earned' in request.data:
            session.tokens_earned = request.data['tokens_earned']
        if 'playtime' in request.data:
            session.playtime = request.data['playtime']
        if 'completed' in request.data:
            session.completed = request.data['completed']
        if 'session_data' in request.data:
            session.session_data = request.data['session_data']
        
        if session.completed and not session.finished_at:
            session.finished_at = timezone.now()
        
        session.save()
        
        # Update overall progress
        if session.completed:
            progress, _ = KindlewickGameProgress.objects.get_or_create(
                user=session.user,
                game_type=session.game_type
            )
            progress.current_level = max(progress.current_level, session.level)
            progress.score += session.score
            progress.tokens_earned += session.tokens_earned
            progress.total_playtime += session.playtime
            progress.save()
        
        serializer = KindlewickGameSessionSerializer(session)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kindlewick_teacher_progress(request):
    """Teacher view: Kindlewick progress for students in their classes."""
    if request.user.role != 'teacher':
        return Response({'error': 'Teacher access only'}, status=status.HTTP_403_FORBIDDEN)

    class_id = request.query_params.get('class_id')
    student_id = request.query_params.get('student_id')
    limit = int(request.query_params.get('limit', 200))

    students = User.objects.filter(enrolled_classes__clazz__teacher=request.user).distinct()
    if class_id:
        students = students.filter(enrolled_classes__clazz_id=class_id)
    if student_id:
        students = students.filter(id=student_id)

    progress = KindlewickGameProgress.objects.filter(user__in=students).select_related('user').order_by('-last_played')[:limit]
    serializer = KindlewickGameProgressAdminSerializer(progress, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kindlewick_teacher_sessions(request):
    """Teacher view: Kindlewick sessions for students in their classes."""
    if request.user.role != 'teacher':
        return Response({'error': 'Teacher access only'}, status=status.HTTP_403_FORBIDDEN)

    class_id = request.query_params.get('class_id')
    student_id = request.query_params.get('student_id')
    limit = int(request.query_params.get('limit', 200))

    students = User.objects.filter(enrolled_classes__clazz__teacher=request.user).distinct()
    if class_id:
        students = students.filter(enrolled_classes__clazz_id=class_id)
    if student_id:
        students = students.filter(id=student_id)

    sessions = KindlewickGameSession.objects.filter(user__in=students).select_related('user').order_by('-created_at')[:limit]
    serializer = KindlewickGameSessionAdminSerializer(sessions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kindlewick_school_admin_progress(request):
    """School admin view: Kindlewick progress for students in the admin's school."""
    if request.user.role != 'school_admin':
        return Response({'error': 'School admin access only'}, status=status.HTTP_403_FORBIDDEN)

    if not request.user.school:
        return Response({'error': 'School association required'}, status=status.HTTP_403_FORBIDDEN)

    class_id = request.query_params.get('class_id')
    student_id = request.query_params.get('student_id')
    teacher_id = request.query_params.get('teacher_id')
    limit = int(request.query_params.get('limit', 300))

    students = User.objects.filter(enrolled_classes__clazz__teacher__school=request.user.school).distinct()
    if teacher_id:
        students = students.filter(enrolled_classes__clazz__teacher_id=teacher_id)
    if class_id:
        students = students.filter(enrolled_classes__clazz_id=class_id)
    if student_id:
        students = students.filter(id=student_id)

    progress = KindlewickGameProgress.objects.filter(user__in=students).select_related('user').order_by('-last_played')[:limit]
    serializer = KindlewickGameProgressAdminSerializer(progress, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kindlewick_school_admin_sessions(request):
    """School admin view: Kindlewick sessions for students in the admin's school."""
    if request.user.role != 'school_admin':
        return Response({'error': 'School admin access only'}, status=status.HTTP_403_FORBIDDEN)

    if not request.user.school:
        return Response({'error': 'School association required'}, status=status.HTTP_403_FORBIDDEN)

    class_id = request.query_params.get('class_id')
    student_id = request.query_params.get('student_id')
    teacher_id = request.query_params.get('teacher_id')
    limit = int(request.query_params.get('limit', 300))

    students = User.objects.filter(enrolled_classes__clazz__teacher__school=request.user.school).distinct()
    if teacher_id:
        students = students.filter(enrolled_classes__clazz__teacher_id=teacher_id)
    if class_id:
        students = students.filter(enrolled_classes__clazz_id=class_id)
    if student_id:
        students = students.filter(id=student_id)

    sessions = KindlewickGameSession.objects.filter(user__in=students).select_related('user').order_by('-created_at')[:limit]
    serializer = KindlewickGameSessionAdminSerializer(sessions, many=True)
    return Response(serializer.data)


# Custom Logout View - Ensures redirect to home
def custom_logout_view(request):
    """Custom logout that explicitly redirects to home"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')
