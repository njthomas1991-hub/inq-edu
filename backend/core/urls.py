from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_page_view, about_page_view, hello, teacher_dashboard_view, teacher_signup_view, student_signup_view, student_signup_with_details_view, create_student_account_view, class_detail_view, add_class_view

urlpatterns = [
    path("", home_page_view, name="home"),
    path("about/", about_page_view, name="about"),
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
]
