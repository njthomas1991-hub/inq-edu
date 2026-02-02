from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_page_view, hello, teacher_dashboard_view

urlpatterns = [
    path("", home_page_view),
    path("api/hello/", hello),
    path("teacher/login/", auth_views.LoginView.as_view(template_name="core/teacher_login.html"), name="teacher_login"),
    path("teacher/", teacher_dashboard_view, name="teacher_dashboard"),
]
