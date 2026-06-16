from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from core.views.auth_views import FlashMessageLoginView, custom_logout_view

from core.views.public_views import (
    home_page_view,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Core app URLs
    path("", include("core.urls")),
    # Home
    path("", home_page_view, name="home"),
    # Auth
    path(
        "login/",
        FlashMessageLoginView.as_view(template_name="core/account/login.html"),
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
