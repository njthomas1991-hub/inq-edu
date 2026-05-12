from django.shortcuts import render


def teacher_dashboard_view(request):
    return render(request, "core/teacher/dashboard.html")


def teacher_analytics_view(request):
    return render(request, "core/teacher/analytics.html")


def class_analytics_view(request):
    return render(request, "core/teacher/class_analytics.html")


def class_detail_view(request):
    return render(request, "core/teacher/class_detail.html")


def add_class_view(request):
    return render(request, "core/teacher/add_class.html")

def account_settings_view(request):
    return render(request, "core/profile/account_settings.html")    