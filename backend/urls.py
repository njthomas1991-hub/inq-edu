from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

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

    # Admin
    path("admin/", admin.site.urls),

    # Core app URLs
    path("", include("core.urls")),

    # Home
    path("", home_page_view, name="home"),

    # Dashboards
    path(
        "teacher/",
        teacher_dashboard_view,
        name="teacher_dashboard",
    ),

    path(
        "student/",
        student_dashboard_view,
        name="student_dashboard",
    ),

    path(
        "school-admin/",
        school_admin_dashboard_view,
        name="school_admin_dashboard",
    ),

    # Auth
    path(
        "login/",
        custom_login_view,
        name="login",
    ),

    path(
        "logout/",
        custom_logout_view,
        name="logout",
    ),

    # Account URLs
    path("", include("core.urls.auth_urls")),

    # Summernote
    path(
        "summernote/",
        include("django_summernote.urls"),
    ),
]

# Static + media in development

if settings.DEBUG:

    urlpatterns += staticfiles_urlpatterns()

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )