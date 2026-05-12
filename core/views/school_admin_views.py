from django.shortcuts import render


def school_admin_dashboard_view(request):
    return render(request, "core/school_admin/dashboard.html")


def school_admin_staff_view(request):
    return render(request, "core/school_admin/staff.html")


def school_admin_classes_view(request):
    return render(request, "core/school_admin/classes.html")


def school_admin_analytics_view(request):
    return render(request, "core/school_admin/analytics.html")


def school_admin_activity_log_view(request):
    return render(request, "core/school_admin/activity_log.html")