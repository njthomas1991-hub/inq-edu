from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q, F
from django.db import models
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
    """Get current logged-in user info, always return JSON"""
    if not request.user.is_authenticated:
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    avatar = getattr(request.user, 'avatar', None)
    user_data = UserSerializer(request.user).data
    user_data['avatar'] = AvatarSerializer(avatar).data if avatar else None
    return Response(user_data)
# 404 JSON handler for base pages
from django.http import JsonResponse, HttpResponseNotFound

def custom_404_view(request, exception=None):
    if request.headers.get('accept', '').startswith('application/json'):
        return JsonResponse({'error': 'Not found'}, status=404)
    return HttpResponseNotFound('<h1>404 Not Found</h1>')


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
    return render(request, "core/teacher_hub.html")
def contact_page_view(request):
    return render(request, "core/contact.html")
def wonderworld_page_view(request):
    return render(request, "core/wonderworld.html")
def hello(request):
    return render(request, "core/hello.html")

def teacher_dashboard_view(request):
    return render(request, "core/teacher_dashboard.html")
def teacher_signup_view(request):
    return render(request, "core/teacher_signup.html")
def student_signup_view(request):
    return render(request, "core/student_signup.html")
def student_signup_with_details_view(request):
    return render(request, "core/student_signup_with_details.html")
def create_student_account_view(request):
    return render(request, "core/create_student_account.html")
def class_detail_view(request):
    return render(request, "core/class_detail.html")
def add_class_view(request):
    return render(request, "core/add_class.html")
def remove_student_view(request):
    return render(request, "core/remove_student.html")
def transfer_student_view(request):
    return render(request, "core/transfer_student.html")
def teacher_news_list_view(request):
    return render(request, "core/teacher_news_list.html")
def teacher_news_detail_view(request):
    return render(request, "core/teacher_news_detail.html")
def teacher_help_list_view(request):
    return render(request, "core/teacher_help_list.html")
def teacher_help_detail_view(request):
    return render(request, "core/teacher_help_detail.html")
def teacher_resources_list_view(request):
    return render(request, "core/teacher_resources_list.html")
def teacher_resource_detail_view(request):
    return render(request, "core/teacher_resource_detail.html")
def teacher_forum_list_view(request):
    return render(request, "core/teacher_forum_list.html")
def teacher_forum_detail_view(request):
    return render(request, "core/teacher_forum_detail.html")
def custom_login_view(request):
    return render(request, "core/custom_login.html")
def student_dashboard_view(request):
    return render(request, "core/student_dashboard.html")
def teacher_forum_delete_view(request):
    return render(request, "core/teacher_forum_delete.html")
def teacher_forum_edit_view(request):
    return render(request, "core/teacher_forum_edit.html")
def teacher_forum_reply_edit_view(request):
    return render(request, "core/teacher_forum_reply_edit.html")
def teacher_forum_reply_delete_view(request):
    return render(request, "core/teacher_forum_reply_delete.html")
def teacher_resource_edit_view(request):
    return render(request, "core/teacher_resource_edit.html")
def teacher_resource_delete_view(request):
    return render(request, "core/teacher_resource_delete.html")
def teacher_resource_comment_delete_view(request):
    return render(request, "core/teacher_resource_comment_delete.html")
def profile_view(request):
    return render(request, "core/profile.html")
def account_settings_view(request):
    return render(request, "core/account_settings.html")
def get_user_avatar(request):
    return render(request, "core/get_user_avatar.html")
def save_user_avatar(request):
    return render(request, "core/save_user_avatar.html")
def randomize_avatar(request):
    return render(request, "core/randomize_avatar.html")
def teacher_analytics_view(request):
    return render(request, "core/teacher_analytics.html")
def class_analytics_view(request):
    return render(request, "core/class_analytics.html")
def student_analytics_view(request):
    return render(request, "core/student_analytics.html")
def school_admin_dashboard_view(request):
    return render(request, "core/school_admin_dashboard.html")
def school_admin_staff_view(request):
    return render(request, "core/school_admin_staff.html")
def school_admin_classes_view(request):
    return render(request, "core/school_admin_classes.html")
def school_admin_analytics_view(request):
    return render(request, "core/school_admin_analytics.html")
def school_admin_activity_log_view(request):
    return render(request, "core/school_admin_activity_log.html")
