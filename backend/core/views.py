from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
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
from .avatar_generator import create_monster_avatar, get_random_avatar_data
from .avatar_renderer import avatar_to_base64
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
                return '/teacher/'  # School admins use teacher dashboard
        return '/teacher/'


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('name', 'subject', 'year_ks', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'year_ks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 4}),
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

    return render(request, "core/student_dashboard.html", {
        "enrollments": enrollments,
        "total_classes": total_classes,
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
        ClassStudent.objects.filter(clazz=class_obj, student_id=student_id).delete()
        
    except Class.DoesNotExist:
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
            return redirect("teacher_dashboard")
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
            return redirect("teacher_resources")
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
            return redirect("teacher_resource_detail", slug=resource.slug)
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
        resource.delete()
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
            return redirect("teacher_forum")
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
def profile_view(request):
    user = request.user
    role = getattr(user, "role", None)

    if role == "teacher":
        classes_taught = user.classes_taught.all()
        template_name = "core/teacher_profile.html"
        context = {
            "classes_taught": classes_taught,
            "classes_count": classes_taught.count(),
        }
    else:
        enrollments = user.enrolled_classes.select_related("clazz").all()
        template_name = "core/student_profile.html"
        context = {
            "enrollments": enrollments,
            "classes_count": enrollments.count(),
        }

    # Add avatar context
    avatar_json = None
    avatar_image = None
    if hasattr(user, 'avatar') and user.avatar:
        avatar_json = json.dumps(user.avatar.to_dict())
        # Generate base64 image for display
        try:
            avatar_image = avatar_to_base64(user.avatar.to_dict(), size=300)
        except Exception as e:
            print(f"Error generating avatar image: {e}")

    context.update({
        "profile_user": user,
        "avatar_json": avatar_json,
        "avatar_image": avatar_image,
    })

    return render(request, template_name, context)


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
            return redirect("teacher_forum_detail", post_id=post.id)
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
        post.delete()
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


@login_required
@require_http_methods(["POST"])
def save_avatar(request):
    """
    Save user's avatar customization and render as PNG image.
    
    Uses Pillow to generate a high-quality PNG image from the avatar data
    and returns it as base64 for immediate display update.
    
    Request body (JSON):
        bodyShape, bodyColor, armStyle, armColor, legStyle, legColor,
        eyeStyle, eyeColor, mouthStyle, mouthColor, hasTeeth, hasGlasses,
        hasEars, hasAntennae, hasShoes, shoeColor
    
    Response:
        {
            'success': True,
            'message': 'Avatar saved successfully',
            'image': '<base64-encoded PNG image>'
        }
    
    The image is rendered using Pillow with all avatar customizations.
    """
    try:
        data = json.loads(request.body)
        
        # Get or create avatar
        avatar, created = Avatar.objects.get_or_create(user=request.user)
        
        # Update avatar fields from request data
        avatar.body_shape = data.get('bodyShape', 'round')
        avatar.body_color = data.get('bodyColor', '#FF6B9D')
        avatar.arm_style = data.get('armStyle', 'short')
        avatar.arm_color = data.get('armColor', '#FF6B9D')
        avatar.leg_style = data.get('legStyle', 'two')
        avatar.leg_color = data.get('legColor', '#FF6B9D')
        avatar.eye_style = data.get('eyeStyle', 'round')
        avatar.eye_color = data.get('eyeColor', '#000000')
        avatar.mouth_style = data.get('mouthStyle', 'smile')
        avatar.mouth_color = data.get('mouthColor', '#000000')
        avatar.has_teeth = data.get('hasTeeth', False)
        avatar.has_glasses = data.get('hasGlasses', False)
        avatar.has_ears = data.get('hasEars', False)
        avatar.has_antennae = data.get('hasAntennae', False)
        avatar.has_shoes = data.get('hasShoes', False)
        avatar.shoe_color = data.get('shoeColor', '#000000')
        
        avatar.save()
        
        # Generate and return avatar image using Pillow
        avatar_image = avatar_to_base64(avatar.to_dict(), size=300)
        
        return JsonResponse({
            'success': True, 
            'message': 'Avatar saved successfully',
            'image': avatar_image
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def generate_random_avatar(request):
    """
    Generate random cute monster avatar data (no save).
    
    Returns avatar configuration data without rendering image.
    Useful for preview before saving.
    
    Response:
        {
            'success': True,
            'avatar': {
                'bodyShape': 'round',
                'bodyColor': '#FF6B9D',
                'armStyle': 'short',
                ... (all avatar fields)
            }
        }
    """
    try:
        avatar_data = get_random_avatar_data()
        return JsonResponse({'success': True, 'avatar': avatar_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["POST"])
def auto_generate_avatar(request):
    """
    Auto-generate and save a cute monster avatar for the current user.
    
    Creates a random cute monster avatar, saves it to database, 
    and renders it as PNG using Pillow.
    
    Response:
        {
            'success': True,
            'message': 'Avatar auto-generated successfully',
            'avatar': { ... avatar data ... },
            'image': '<base64-encoded PNG image>'
        }
    
    The Pillow-rendered image can be displayed immediately with:
        <img src="data:image/png;base64,{{ image }}" />
    """
    try:
        avatar = create_monster_avatar(user=request.user, cute_bias=True)
        avatar_image = avatar_to_base64(avatar.to_dict(), size=300)
        return JsonResponse({
            'success': True,
            'message': 'Avatar auto-generated successfully',
            'avatar': avatar.to_dict(),
            'image': avatar_image
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def get_avatar_image(request):
    """
    Get base64 PNG image of user's current avatar.
    
    Renders existing avatar to PNG using Pillow and returns 
    base64-encoded image for display.
    
    Response:
        {
            'success': True,
            'image': '<base64-encoded PNG image>'
        }
    
    Error if no avatar exists:
        {
            'success': False,
            'error': 'No avatar found'
        }
    """
    try:
        if hasattr(request.user, 'avatar') and request.user.avatar:
            avatar_image = avatar_to_base64(request.user.avatar.to_dict(), size=300)
            return JsonResponse({
                'success': True,
                'image': avatar_image
            })
        else:
            return JsonResponse({'success': False, 'error': 'No avatar found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)



