from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home_page_view, about_page_view, kindlewick_page_view, questopia_page_view, pricing_page_view,
    teacher_hub_view, contact_page_view, wonderworld_page_view, hello, teacher_dashboard_view,
    teacher_signup_view, student_signup_view, student_signup_with_details_view,
    create_student_account_view, class_detail_view, add_class_view, remove_student_view,
    transfer_student_view, teacher_news_list_view, teacher_news_detail_view,
    teacher_help_list_view, teacher_help_detail_view, teacher_resources_list_view,
    teacher_resource_detail_view, teacher_forum_list_view, teacher_forum_detail_view,
    custom_login_view, student_dashboard_view
)

urlpatterns = [
    path("", home_page_view, name="home"),
    path("about/", about_page_view, name="about"),
    path("kindlewick/", kindlewick_page_view, name="kindlewick"),
    path("wonderworld/", wonderworld_page_view, name="wonderworld"),
    path("questopia/", questopia_page_view, name="questopia"),
    path("pricing/", pricing_page_view, name="pricing"),
    path("teacher-hub/", teacher_hub_view, name="teacher_hub"),
    path("contact/", contact_page_view, name="contact"),
    path("api/hello/", hello),
    path("teacher/signup/", teacher_signup_view, name="signup"),
    path("student/signup/", student_signup_view, name="student_signup"),
    path("student/signup/guided/", student_signup_with_details_view, name="student_signup_guided"),
    path("api/create-student/", create_student_account_view, name="create_student"),
    path("student/", student_dashboard_view, name="student_dashboard"),
    path("teacher/login/", custom_login_view, name="teacher_login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("teacher/", teacher_dashboard_view, name="teacher_dashboard"),
    path("teacher/class/add/", add_class_view, name="add_class"),
    path("teacher/class/<int:class_id>/", class_detail_view, name="class_detail"),
    path("teacher/class/<int:class_id>/remove/<int:student_id>/", remove_student_view, name="remove_student"),
    path("teacher/class/<int:class_id>/transfer/<int:student_id>/", transfer_student_view, name="transfer_student"),
    path("teacher/news/", teacher_news_list_view, name="teacher_news"),
    path("teacher/news/<slug:slug>/", teacher_news_detail_view, name="teacher_news_detail"),
    path("teacher/help/", teacher_help_list_view, name="teacher_help"),
    path("teacher/help/<slug:slug>/", teacher_help_detail_view, name="teacher_help_detail"),
    path("teacher/resources/", teacher_resources_list_view, name="teacher_resources"),
    path("teacher/resources/<slug:slug>/", teacher_resource_detail_view, name="teacher_resource_detail"),
    path("teacher/forum/", teacher_forum_list_view, name="teacher_forum"),
    path("teacher/forum/<int:post_id>/", teacher_forum_detail_view, name="teacher_forum_detail"),
]
