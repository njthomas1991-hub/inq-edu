from django.shortcuts import render


def student_dashboard_view(request):
    return render(request, "core/student/dashboard.html")


def student_analytics_view(request):
    return render(request, "core/student/analytics.html")