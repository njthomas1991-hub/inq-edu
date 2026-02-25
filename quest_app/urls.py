from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("teacher-dashboard/", views.dashboard, name="teacher_dashboard"),
    path(
        "teacher-analytics/",
        TemplateView.as_view(template_name="core/teacher_analytics.html"),
        name="teacher_analytics",
    ),
    path("add-class/", views.add_class, name="add_class"),
    path("api/add-class/", views.add_class_ajax, name="add_class_api"),
    path("class/<int:pk>/edit/", views.edit_class, name="edit_class"),
    path("class/<int:pk>/archive/", views.archive_class, name="archive_class"),
    path("classes/", views.classes_list, name="classes"),
    path("class/<int:pk>/", views.class_detail, name="class_detail"),
    path("api/create-student/", views.create_student_api, name="create_student_api"),
    path("api/student/login/", views.student_login_api, name="student_login_api"),
    path("class/<int:pk>/print-cards/", views.print_student_cards, name="print_student_cards"),
    path("class/<int:pk>/print-cards/pdf/", views.print_student_cards_pdf, name="print_student_cards_pdf"),
    path("class/<int:class_pk>/print-cards/email/<int:student_id>/", views.email_student_card_pdf, name="email_student_card_pdf"),
    path("class/<int:pk>/promote/", views.promote_class, name="promote_class"),
    path(
        "teacher-news/",
        TemplateView.as_view(template_name="core/teacher_news_list.html"),
        name="teacher_news",
    ),
    path(
        "teacher-help/",
        TemplateView.as_view(template_name="core/teacher_help_list.html"),
        name="teacher_help",
    ),
    path("teacher-resources/", views.teacher_resources, name="teacher_resources"),
    path("resource/<int:pk>/edit/", views.resource_edit, name="resource_edit"),
    path("resource/<int:pk>/delete/", views.resource_delete, name="resource_delete"),
    path("resource/<int:pk>/comment/", views.resource_comment, name="resource_comment"),
    path(
        "teacher-forum/",
        TemplateView.as_view(template_name="core/teacher_forum.html"),
        name="teacher_forum",
    ),
    path(
        "account-settings/",
        TemplateView.as_view(template_name="core/account_settings.html"),
        name="account_settings",
    ),
    path("profile/", views.profile, name="profile"),
    path("api/generate-reset/", views.generate_reset_api, name="generate_reset_api"),
    path("api/student-password/<int:pk>/", views.reveal_student_password, name="reveal_student_password"),
    path("student-reset/<str:token>/", views.student_reset, name="student_reset"),
    path("archived-students/", views.archived_students, name="archived_students"),
    path("api/summernote-upload/", views.summernote_upload, name="summernote_upload"),
    # Avatar API endpoints
    path("api/avatar/", views.avatar_api, name="avatar_api"),
    path("api/avatar/save/", views.avatar_save, name="avatar_save"),
    path("api/avatar/randomize/", views.avatar_randomize, name="avatar_randomize"),
    path("api/profile/update/", views.profile_update, name="profile_update"),
    path(
        "kindlewick/",
        TemplateView.as_view(template_name="core/kindlewick.html"),
        name="kindlewick",
    ),
    path(
        "wonderworld/",
        TemplateView.as_view(template_name="core/wonderworld.html"),
        name="wonderworld",
    ),
    path(
        "questopia/",
        TemplateView.as_view(template_name="core/questopia.html"),
        name="questopia",
    ),
    path(
        "contact/",
        TemplateView.as_view(template_name="core/contact.html"),
        name="contact",
    ),
    path(
        "teacher-hub/",
        TemplateView.as_view(template_name="core/teacher_hub.html"),
        name="teacher_hub",
    ),
    # JWT token endpoints for API clients
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
