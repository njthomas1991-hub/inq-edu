from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='core/about.html'), name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher-dashboard/', views.dashboard, name='teacher_dashboard'),
    path('teacher-analytics/', TemplateView.as_view(template_name='core/teacher_analytics.html'), name='teacher_analytics'),
    path('add-class/', TemplateView.as_view(template_name='core/add_class.html'), name='add_class'),
    path('teacher-news/', TemplateView.as_view(template_name='core/teacher_news_list.html'), name='teacher_news'),
    path('teacher-help/', TemplateView.as_view(template_name='core/teacher_help_list.html'), name='teacher_help'),
    path('teacher-resources/', TemplateView.as_view(template_name='core/teacher_resources_list.html'), name='teacher_resources'),
    path('teacher-forum/', TemplateView.as_view(template_name='core/teacher_forum.html'), name='teacher_forum'),
    path('account-settings/', TemplateView.as_view(template_name='core/account_settings.html'), name='account_settings'),
    path('profile/', views.profile, name='profile'),
    path('kindlewick/', TemplateView.as_view(template_name='core/kindlewick.html'), name='kindlewick'),
    path('wonderworld/', TemplateView.as_view(template_name='core/wonderworld.html'), name='wonderworld'),
    path('questopia/', TemplateView.as_view(template_name='core/questopia.html'), name='questopia'),
    path('contact/', TemplateView.as_view(template_name='core/contact.html'), name='contact'),
    path('teacher-hub/', TemplateView.as_view(template_name='core/teacher_hub.html'), name='teacher_hub'),
]
