from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # Core app URLs (includes public, auth, teacher, student, profile, API, legal)
    path("", include("core.urls")),
    
    # Summernote
    path("summernote/", include("django_summernote.urls")),
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
