from django.urls import path

from core.views.student_views import (
    student_signup_with_details_view,
    create_student_account_view,
    student_dashboard_view,
)

urlpatterns = [
    path("student/signup/", student_signup_with_details_view, name="student_signup"),
    path(
        "student/signup/guided/",
        student_signup_with_details_view,
        name="student_signup_guided",
    ),
    path("student/", student_dashboard_view, name="student_dashboard"),
]
