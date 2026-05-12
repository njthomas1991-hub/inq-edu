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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from core.views.auth_views import (
    custom_login_view,
    custom_logout_view,
)

from core.views.public_views import (
    home_page_view,
)

from core.views.teacher_views import (
    teacher_dashboard_view,
)

from core.views.student_views import (
    student_dashboard_view,
)

from core.views.school_admin_views import (
    school_admin_dashboard_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path("", home_page_view, name="home"),
    path("teacher/", teacher_dashboard_view, name="teacher_dashboard"),
    path("student/", student_dashboard_view, name="student_dashboard"),
    path("school-admin/", school_admin_dashboard_view, name="school_admin_dashboard"),
    path('summernote/', include('django_summernote.urls')),
    path("login/", custom_login_view, name="login"),
    path("logout/", custom_logout_view, name="logout"),
    path("accounts/", include("allauth.urls")),
]   

# Serve static files (images/css/js) during development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
