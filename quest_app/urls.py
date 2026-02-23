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
    path('profile/', views.profile, name='profile'),
    path('kindlewick/', TemplateView.as_view(template_name='core/kindlewick.html'), name='kindlewick'),
    path('wonderworld/', TemplateView.as_view(template_name='core/wonderworld.html'), name='wonderworld'),
    path('questopia/', TemplateView.as_view(template_name='core/questopia.html'), name='questopia'),
    path('contact/', TemplateView.as_view(template_name='core/contact.html'), name='contact'),
    path('teacher-hub/', TemplateView.as_view(template_name='core/teacher_hub.html'), name='teacher_hub'),
]
