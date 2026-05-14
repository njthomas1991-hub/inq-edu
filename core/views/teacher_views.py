import csv

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from core.forms.class_forms import CreateStudentForm
from core.models import Class, ForumPost, ForumReply, ResourceComment, TeachingResource, User


@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def add_student_view(request):
    """
    Teacher-created student accounts.
    Creates real User records with role='student', generated password, saved to DB.
    """
    if request.method == 'GET':
        form = CreateStudentForm()
        return render(request, "core/teacher/add_student.html", {'form': form})

    if request.method == 'POST':
        form = CreateStudentForm(request.POST)

        if form.is_valid():
            student = form.save()

            recent_ids = request.session.get('recent_student_ids', [])
            recent_ids.append(int(student.pk))
            request.session['recent_student_ids'] = recent_ids[-100:]

            return render(request, "core/teacher/add_student.html", {
                'form': CreateStudentForm(),
                'created_student': student,
            })

        return render(request, "core/teacher/add_student.html", {
            'form': form,
        })

    return render(request, "core/teacher/add_student.html", {
        'form': CreateStudentForm(),
    })


@login_required
@require_http_methods(["GET"])
def download_student_login_card_view(request, student_id):
    """Download a plain-text login card for a student account."""
    student = get_object_or_404(
        User,
        id=student_id,
        role='student',
        school=request.user.school
    )

    card_lines = [
        "Inq-Ed Student Login Card",
        "=========================",
        f"Student Name: {(student.get_full_name() or student.username).strip()}",
        f"Username: {student.username}",
        f"Password: {student.plain_password or '[Password not available]'}",
        "Login URL: /login/",
    ]

    response = HttpResponse("\n".join(card_lines), content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="student-login-card-{student.username}.txt"'
    return response


@login_required
@require_http_methods(["GET"])
def download_recent_student_login_cards_csv_view(request):
    """Download CSV login cards for recently created student accounts."""
    if getattr(request.user, 'role', None) not in ['teacher', 'school_admin']:
        return HttpResponseForbidden("You do not have permission to download student login cards.")

    recent_ids = request.session.get('recent_student_ids', [])
    students = User.objects.filter(id__in=recent_ids, role='student').order_by('id')

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="recent-student-login-cards.csv"'

    writer = csv.writer(response)
    writer.writerow(["first_name", "last_name", "username", "password", "login_url"])

    for student in students:
        writer.writerow([
            student.first_name,
            student.last_name,
            student.username,
            student.plain_password or "",
            "/login/",
        ])

    return response


def teacher_dashboard_view(request):
    return render(request, "core/teacher/teacher_dashboard.html")


def teacher_analytics_view(request):
    return render(request, "core/teacher/analytics/teacher_analytics.html")


@login_required
def class_analytics_view(request, class_id=None):
    if class_id:
        clazz = get_object_or_404(
            Class,
            id=class_id,
            teacher__school=request.user.school
        )
        return render(request, "core/teacher/classes/class_analytics.html", {"class": clazz})
    return render(request, "core/teacher/classes/class_analytics.html")


@login_required
def student_analytics_view(request, class_id=None, student_id=None):
    if class_id and student_id:
        clazz = get_object_or_404(
            Class,
            id=class_id,
            teacher__school=request.user.school
        )
        student = get_object_or_404(
            User,
            id=student_id,
            role='student',
            enrolled_classes__clazz=clazz
        )
        return render(request, "core/student/student_analytics.html", {"class": clazz, "student": student})
    return render(request, "core/student/student_analytics.html")


def add_class_view(request):
    return render(request, "core/teacher/classes/add.html")


@login_required
def class_detail_view(request, class_id):
    clazz = get_object_or_404(
        Class,
        id=class_id,
        teacher__school=request.user.school
    )
    return render(request, "core/teacher/classes/class_detail.html", {"class": clazz})


@login_required
def remove_student_view(request, class_id, student_id):
    clazz = get_object_or_404(
        Class,
        id=class_id,
        teacher__school=request.user.school
    )
    student = get_object_or_404(
        User,
        id=student_id,
        role='student',
        enrolled_classes__clazz=clazz
    )
    return render(request, "core/teacher/classes/remove_student.html", {"class": clazz, "student": student})


@login_required
def transfer_student_view(request, class_id, student_id):
    clazz = get_object_or_404(
        Class,
        id=class_id,
        teacher__school=request.user.school
    )
    student = get_object_or_404(
        User,
        id=student_id,
        role='student',
        enrolled_classes__clazz=clazz
    )
    return render(request, "core/teacher/classes/transfer_student.html", {"class": clazz, "student": student})


def teacher_news_list_view(request):
    return render(request, "core/teacher/news/teacher_news_list.html")


def teacher_news_detail_view(request, slug):
    return render(request, "core/teacher/news/teacher_news_detail.html")


def teacher_help_list_view(request):
    return render(request, "core/teacher/guides/teacher_help_list.html")


def teacher_help_detail_view(request, slug):
    return render(request, "core/teacher/guides/teacher_help_detail.html")


@login_required
def teacher_resources_list_view(request):
    """List teaching resources visible to the current user based on visibility and school."""
    from django.db.models import Q
    
    # Show all own resources + school resources + public resources
    resources = TeachingResource.objects.filter(
        Q(author=request.user) |  # Own resources
        Q(visibility='public') |  # Public resources from anyone
        Q(visibility='school', author__school=request.user.school)  # School resources from same school
    ).select_related('author').filter(status='published').order_by('-published_at')
    
    return render(request, "core/teacher/resources/teacher_resources_list.html", {"resources": resources})


@login_required
def teacher_resource_detail_view(request, slug):
    """Display a resource if user has permission based on visibility and school."""
    from django.db.models import Q
    
    resource = get_object_or_404(
        TeachingResource,
        slug=slug,
        status='published'
    )
    
    # Check permissions: own resource, public resource, or school-only from same school
    if resource.author != request.user:
        if resource.visibility == 'school' and resource.author.school != request.user.school:
            raise Http404("You don't have permission to view this resource.")
        elif resource.visibility != 'public' and resource.visibility != 'school':
            raise Http404("You don't have permission to view this resource.")
    
    return render(request, "core/teacher/resources/teacher_resource_detail.html", {"resource": resource})


@login_required
def teacher_resource_edit_view(request, slug):
    resource = get_object_or_404(
        TeachingResource,
        slug=slug,
        author__school=request.user.school
    )
    return render(request, "core/teacher/resources/teacher_resource_form.html", {"resource": resource})


@login_required
def teacher_resource_delete_view(request, slug):
    resource = get_object_or_404(
        TeachingResource,
        slug=slug,
        author__school=request.user.school
    )
    return render(request, "core/teacher/resources/teacher_resource_delete.html", {"resource": resource})


@login_required
def teacher_resource_comment_delete_view(request, slug, comment_id):
    resource = get_object_or_404(
        TeachingResource,
        slug=slug,
        author__school=request.user.school
    )
    comment = get_object_or_404(
        ResourceComment,
        id=comment_id,
        resource=resource
    )
    return render(request, "core/teacher/resources/teacher_resource_comment_delete.html", {"resource": resource, "comment": comment})


def teacher_forum_list_view(request):
    return render(request, "core/teacher/forum/teacher_forum_list.html")


@login_required
def teacher_forum_detail_view(request, post_id):
    post = get_object_or_404(
        ForumPost,
        id=post_id,
        author__school=request.user.school
    )
    return render(request, "core/teacher/forum/teacher_forum_detail.html", {"post": post})


@login_required
def teacher_forum_edit_view(request, post_id):
    post = get_object_or_404(
        ForumPost,
        id=post_id,
        author__school=request.user.school
    )
    return render(request, "core/teacher/forum/teacher_forum_form.html", {"post": post})


@login_required
def teacher_forum_delete_view(request, post_id):
    post = get_object_or_404(
        ForumPost,
        id=post_id,
        author__school=request.user.school
    )
    return render(request, "core/teacher/forum/teacher_forum_delete.html", {"post": post})


@login_required
def teacher_forum_reply_edit_view(request, post_id, reply_id):
    post = get_object_or_404(
        ForumPost,
        id=post_id,
        author__school=request.user.school
    )
    reply = get_object_or_404(
        ForumReply,
        id=reply_id,
        post=post
    )
    return render(request, "core/teacher/forum/teacher_forum_reply_edit.html", {"post": post, "reply": reply})


@login_required
def teacher_forum_reply_delete_view(request, post_id, reply_id):
    post = get_object_or_404(
        ForumPost,
        id=post_id,
        author__school=request.user.school
    )
    reply = get_object_or_404(
        ForumReply,
        id=reply_id,
        post=post
    )
    return render(request, "core/teacher/forum/teacher_forum_reply_delete.html", {"post": post, "reply": reply})