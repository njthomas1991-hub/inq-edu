from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("quest_app.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom 404 handler (dotted path or callable). Keep assignment after imports.
handler404 = "django.shortcuts.render"
