from django.shortcuts import render


def student_dashboard_view(request):
    return render(request, "core/student/student_dashboard.html")


def student_signup_with_details_view(request):
    return render(request, "core/student/student_signup_with_details.html")


def create_student_account_view(request):
    return render(request, "core/student/create_student_account.html")
