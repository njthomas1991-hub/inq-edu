from django.urls import path

from core.views.school_admin_views import (
    school_admin_dashboard_view,
    school_admin_staff_view,
    school_admin_classes_view,
    school_admin_analytics_view,
    school_admin_activity_log_view,
)

urlpatterns = [
    path("school-admin/", school_admin_dashboard_view, name="school_admin_dashboard"),
    path("school-admin/staff/", school_admin_staff_view, name="school_admin_staff"),
    path(
        "school-admin/classes/", school_admin_classes_view, name="school_admin_classes"
    ),
    path(
        "school-admin/analytics/",
        school_admin_analytics_view,
        name="school_admin_analytics",
    ),
    path(
        "school-admin/activity/",
        school_admin_activity_log_view,
        name="school_admin_activity_log",
    ),
]
