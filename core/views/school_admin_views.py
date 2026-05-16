from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import render

from core.models import Class, TeachingResource, User


def _require_school_admin(request):
    if getattr(request.user, "role", None) != "school_admin":
        return HttpResponseForbidden("You do not have permission to access this page.")
    return None


@login_required
def school_admin_dashboard_view(request):
    forbidden = _require_school_admin(request)
    if forbidden:
        return forbidden

    school = request.user.school
    if not school:
        return HttpResponseForbidden("You do not have an assigned school.")

    teachers = User.objects.filter(role="teacher", school=school)
    students = User.objects.filter(role="student", school=school)
    classes = Class.objects.filter(teacher__school=school).select_related("teacher")
    resources = TeachingResource.objects.filter(author__school=school).select_related("author")

    return render(request, "core/school_admin/dashboard.html", {
        "school_name": school.name,
        "school": school,
        "teachers_count": teachers.count(),
        "students_count": students.count(),
        "classes_count": classes.count(),
        "resources_count": resources.count(),
        "recent_classes": classes.order_by("-created_at")[:5],
        "recent_logins": User.objects.filter(
            school=school,
            last_login__isnull=False,
        ).order_by("-last_login")[:5],
    })


@login_required
def school_admin_staff_view(request):
    forbidden = _require_school_admin(request)
    if forbidden:
        return forbidden

    school = request.user.school
    if not school:
        return HttpResponseForbidden("You do not have an assigned school.")

    teachers = User.objects.filter(role="teacher", school=school).annotate(class_count=Count("classes_taught"))

    return render(request, "core/school_admin/staff.html", {
        "school_name": school.name,
        "school": school,
        "teachers": teachers,
    })


@login_required
def school_admin_classes_view(request):
    forbidden = _require_school_admin(request)
    if forbidden:
        return forbidden

    school = request.user.school
    if not school:
        return HttpResponseForbidden("You do not have an assigned school.")

    classes = Class.objects.filter(teacher__school=school).select_related("teacher").annotate(student_count=Count("students"))

    return render(request, "core/school_admin/classes.html", {
        "school_name": school.name,
        "school": school,
        "classes": classes,
    })


@login_required
def school_admin_analytics_view(request):
    forbidden = _require_school_admin(request)
    if forbidden:
        return forbidden

    school = request.user.school
    if not school:
        return HttpResponseForbidden("You do not have an assigned school.")

    classes = Class.objects.filter(teacher__school=school)
    students = User.objects.filter(role="student", school=school)

    subject_breakdown = []
    for subject_value, subject_label in Class.SUBJECT_CHOICES:
        count = classes.filter(subject=subject_value).count()
        if count:
            subject_breakdown.append({"label": subject_label, "count": count})

    year_ks_breakdown = []
    for year_ks_value, year_ks_label in Class.year_ks_CHOICES:
        count = classes.filter(year_ks=year_ks_value).count()
        if count:
            year_ks_breakdown.append({"label": year_ks_label, "count": count})

    return render(request, "core/school_admin/analytics.html", {
        "school_name": school.name,
        "school": school,
        "classes_count": classes.count(),
        "total_students": students.count(),
        "subject_breakdown": subject_breakdown,
        "year_ks_breakdown": year_ks_breakdown,
        "classes": classes.select_related("teacher"),
        "per_game_stats": [],
    })


@login_required
def school_admin_activity_log_view(request):
    forbidden = _require_school_admin(request)
    if forbidden:
        return forbidden

    school_name = request.user.school
    recent_classes = Class.objects.filter(teacher__school=school_name).select_related("teacher").order_by("-created_at")[:20]
    recent_resources = TeachingResource.objects.filter(author__school=school_name).select_related("author").order_by("-created_at")[:20]

    return render(request, "core/school_admin/activity_log.html", {
        "school_name": school_name,
        "recent_classes": recent_classes,
        "recent_resources": recent_resources,
    })