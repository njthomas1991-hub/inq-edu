from django.urls import path, include

handler404 = 'core.views.custom_404_view'

urlpatterns = [
    path('', include('core.urls.public_urls')),
    path('', include('core.urls.auth_urls')),
    path('', include('core.urls.teacher_urls')),
    path('', include('core.urls.student_urls')),
    path('', include('core.urls.school_admin_urls')),
    path('', include('core.urls.api_urls')),
    path('', include('core.urls.legal_urls')),
]