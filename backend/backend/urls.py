"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from core import views

urlpatterns = [
    path('', include('core.urls')),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('wonderworld/', views.wonderworld, name='wonderworld'),
    path('questopia/', views.questopia, name='questopia'),
    path('kindlewick/', views.kindlewick, name='kindlewick'),
    path('pricing/', views.pricing, name='pricing'),
    path('teacher_hub/', views.teacher_hub, name='teacher_hub'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
]

# Serve static files (images/css/js) during development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
