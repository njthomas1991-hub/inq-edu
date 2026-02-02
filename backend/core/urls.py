from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_page_view, about_page_view, kindlewick_page_view, questopia_page_view, pricing_page_view, teacher_hub_view, contact_page_view, hello, teacher_dashboard_view, teacher_signup_view, student_signup_view, student_signup_with_details_view, create_student_account_view, class_detail_view, add_class_view, remove_student_view

urlpatterns = [
    path("", home_page_view, name="home"),
    path("about/", about_page_view, name="about"),
    path("kindlewick/", kindlewick_page_view, name="kindlewick"),
    path("questopia/", questopia_page_view, name="questopia"),
    path("pricing/", pricing_page_view, name="pricing"),
    path("teacher-hub/", teacher_hub_view, name="teacher_hub"),
    path("contact/", contact_page_view, name="contact"),
    path("api/hello/", hello),
    path("teacher/signup/", teacher_signup_view, name="signup"),
    path("student/signup/", student_signup_view, name="student_signup"),
    path("student/signup/guided/", student_signup_with_details_view, name="student_signup_guided"),
    path("api/create-student/", create_student_account_view, name="create_student"),
    path("teacher/login/", auth_views.LoginView.as_view(template_name="core/teacher_login.html"), name="teacher_login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("teacher/", teacher_dashboard_view, name="teacher_dashboard"),
    path("teacher/class/add/", add_class_view, name="add_class"),
    path("teacher/class/<int:class_id>/", class_detail_view, name="class_detail"),
    path("teacher/class/<int:class_id>/remove/<int:student_id>/", remove_student_view, name="remove_student"),
]
