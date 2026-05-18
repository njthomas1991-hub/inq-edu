import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from core.models import (
    User,
    Class,
    ClassStudent,
    TeachingResource,
    ForumPost,
)

from core.forms.class_forms import (
    ClassForm,
    ClassGroupEditForm,
)

from core.forms.resource_forms import (
    TeachingResourceForm,
)

from core.forms.forum_forms import (
    ForumPostForm,
    ForumReplyForm,
)


# =====================================================
# HELPERS
# =====================================================

def teacher_required(user):

    return (
        user.is_authenticated
        and user.role in [
            "teacher",
            "school_admin",
        ]
    )


WORD_LIST = [
    "Blue",
    "Tiger",
    "Rocket",
    "Apple",
    "Magic",
    "Sunny",
    "Forest",
    "Dragon",
    "River",
    "Star",
    "Cloud",
    "Ocean",
]


def generate_username(first_name, last_name):

    base = (
        first_name.lower() +
        (
            last_name[0].lower()
            if last_name else ""
        )
    )

    username = base
    counter = 1

    while User.objects.filter(
        username=username
    ).exists():

        counter += 1
        username = f"{base}{counter}"

    return username


def generate_password():

    return (
        random.choice(WORD_LIST) +
        random.choice(WORD_LIST)
    )


# =====================================================
# DASHBOARD
# =====================================================

@login_required
def teacher_dashboard_view(request):

    classes = Class.objects.filter(
        teacher=request.user
    )

    resources = TeachingResource.objects.filter(
        author=request.user
    )[:5]

    forum_posts = ForumPost.objects.filter(
        author=request.user
    )[:5]

    context = {
        "classes": classes,
        "resources": resources,
        "forum_posts": forum_posts,
    }

    return render(
        request,
        "core/teacher/teacher_dashboard.html",
        context,
    )


# =====================================================
# CLASSES
# =====================================================

@login_required
def teacher_classes_view(request):

    classes = Class.objects.filter(
        teacher=request.user
    )

    context = {
        "classes": classes,
    }

    return render(
        request,
        "core/teacher/classes/class_list.html",
        context,
    )


@login_required
def class_detail_view(request, pk):

    class_obj = get_object_or_404(
        Class,
        pk=pk,
        teacher=request.user,
    )

    students = ClassStudent.objects.filter(
        clazz=class_obj
    ).select_related("student")

    teacher_classes = Class.objects.filter(
        teacher=request.user
    )

    new_student = request.session.pop(
        "new_student",
        None,
    )

    context = {
        "class_obj": class_obj,
        "students": students,
        "teacher_classes": teacher_classes,
        "new_student": new_student,
    }

    return render(
        request,
        "core/teacher/classes/class_detail.html",
        context,
    )


@login_required
def create_class_view(request):

    if request.method == "POST":

        form = ClassForm(request.POST)

        if form.is_valid():

            classroom = form.save(
                commit=False
            )

            classroom.teacher = request.user
            classroom.save()

            messages.success(
                request,
                "Class created successfully.",
            )

            return redirect(
                "teacher_classes"
            )

    else:

        form = ClassForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "core/teacher/classes/class_form.html",
        context,
    )


@login_required
def edit_class_view(request, pk):

    classroom = get_object_or_404(
        Class,
        pk=pk,
        teacher=request.user,
    )

    if request.method == "POST":

        form = ClassForm(
            request.POST,
            instance=classroom,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Class updated successfully.",
            )

            return redirect(
                "class_detail",
                pk=classroom.pk,
            )

    else:

        form = ClassForm(
            instance=classroom
        )

    context = {
        "form": form,
        "classroom": classroom,
    }

    return render(
        request,
        "core/teacher/classes/class_form.html",
        context,
    )


@login_required
def delete_class_view(request, pk):

    classroom = get_object_or_404(
        Class,
        pk=pk,
        teacher=request.user,
    )

    if request.method == "POST":

        classroom.delete()

        messages.success(
            request,
            "Class deleted successfully.",
        )

        return redirect(
            "teacher_classes"
        )

    context = {
        "classroom": classroom,
    }

    return render(
        request,
        "core/teacher/classes/class_delete.html",
        context,
    )


@login_required
def teacher_class_edit_view(
    request,
    slug
):

    class_group = get_object_or_404(

        Class,

        slug=slug,
    )

    if request.method == "POST":

        form = ClassGroupEditForm(

            request.POST,

            instance=class_group,

            school=request.user.school,
        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Class updated successfully.",
            )

            return redirect(
                "teacher_classes"
            )

    else:

        form = ClassGroupEditForm(

            instance=class_group,

            school=request.user.school,
        )

    return render(

        request,

        "core/teacher/classes/class_edit.html",

        {
            "form": form,
            "class_group": class_group,
        },
    )


@login_required
def teacher_class_delete_view(
    request,
    slug
):

    class_group = get_object_or_404(

        Class,

        slug=slug,
    )

    if request.method == "POST":

        class_group.delete()

        messages.success(

            request,

            "Class deleted successfully.",
        )

        return redirect(
            "teacher_classes"
        )

    return redirect(
        "teacher_classes"
    )


# =====================================================
# STUDENTS
# =====================================================

@login_required
def add_student_to_class_view(request, pk):

    teacher_class = get_object_or_404(
        Class,
        pk=pk,
    )

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name"
        )

        last_name = request.POST.get(
            "last_name"
        )

        username = generate_username(
            first_name,
            last_name,
        )

        password = generate_password()

        student = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role="student",
            school=request.user.school,
        )
        student.plain_password = password
        student.save()

        ClassStudent.objects.create(
            student=student,
            clazz=teacher_class,
        )

        request.session["new_student"] = {
            "full_name": f"{first_name} {last_name}",
            "username": username,
            "password": password,
        }

        messages.success(
            request,
            "Student created successfully.",
        )

        return redirect(
            "class_detail",
            pk=teacher_class.pk,
        )

    context = {
        "teacher_class": teacher_class,
    }

    return render(
        request,
        "core/teacher/classes/add_student.html",
        context,
    )

@login_required
def remove_student_view(
    request,
    class_pk,
    student_pk,
    ):

    classroom = get_object_or_404(
        Class,
        pk=class_pk,
        teacher=request.user,
    )

    enrollment = get_object_or_404(
        ClassStudent,
        clazz=classroom,
        student_id=student_pk,
    )

    if request.method == "POST":

        enrollment.delete()

        messages.success(
            request,
            "Student removed from class.",
        )

        return redirect(
            "class_detail",
            pk=classroom.pk,
        )

    context = {
        "classroom": classroom,
        "enrollment": enrollment,
    }

    return render(
        request,
        "core/teacher/classes/remove_student.html",
        context,
    )

@login_required
def transfer_student_view(
    request,
    class_pk,
    student_pk,
    ):

    current_class = get_object_or_404(
        Class,
        pk=class_pk,
        teacher=request.user,
    )

    enrollment = get_object_or_404(
        ClassStudent,
        clazz=current_class,
        student_id=student_pk,
    )

    if request.method == "POST":

        target_class_id = request.POST.get(
            "target_class_id"
        )

        target_class = get_object_or_404(
            Class,
            pk=target_class_id,
            teacher=request.user,
        )

        enrollment.clazz = target_class
        enrollment.save()

        messages.success(
            request,
            "Student transferred successfully.",
        )

        return redirect(
            "class_detail",
            pk=target_class.pk,
        )

    teacher_classes = Class.objects.filter(
        teacher=request.user
    ).exclude(
        pk=current_class.pk
    )

    context = {
        "current_class": current_class,
        "enrollment": enrollment,
        "teacher_classes": teacher_classes,
    }

    return render(
        request,
        "core/teacher/classes/transfer_student.html",
        context,
    )


# =====================================================
# RESOURCES CRUD
# =====================================================

@login_required
def teacher_resources_list_view(request):

    resources = TeachingResource.objects.filter(
        author=request.user
    )

    form = TeachingResourceForm()

    context = {
        "resources": resources,
        "form": form,
    }

    return render(
        request,
        "core/teacher/resources/teacher_resources_list.html",
        context,
    )

@login_required
def teacher_resource_create_view(request):

    if request.method == "POST":

        form = TeachingResourceForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            resource = form.save(
                commit=False
            )

            resource.author = request.user
            resource.save()

            messages.success(
                request,
                "Resource created successfully.",
            )

            return redirect(
                "teacher_resource_detail",
                pk=resource.pk,
            )

    else:

        form = TeachingResourceForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "core/teacher/resources/teacher_resource_form.html",
        context,
    )


@login_required
def teacher_resource_detail_view(request, pk):

    resource = get_object_or_404(
        TeachingResource,
        pk=pk,
        author=request.user,
    )

    context = {
        "resource": resource,
    }

    return render(
        request,
        "core/teacher/resources/teacher_resource_detail.html",
        context,
    )


@login_required
def teacher_resource_edit_view(request, pk):

    resource = get_object_or_404(
        TeachingResource,
        pk=pk,
        author=request.user,
    )

    if request.method == "POST":

        form = TeachingResourceForm(
            request.POST,
            request.FILES,
            instance=resource,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Resource updated successfully.",
            )

            return redirect(
                "teacher_resource_detail",
                pk=resource.pk,
            )

    else:

        form = TeachingResourceForm(
            instance=resource
        )

    context = {
        "form": form,
        "resource": resource,
    }

    return render(
        request,
        "core/teacher/resources/teacher_resource_form.html",
        context,
    )


@login_required
def teacher_resource_delete_view(request, pk):

    resource = get_object_or_404(
        TeachingResource,
        pk=pk,
        author=request.user,
    )

    if request.method == "POST":

        resource.delete()

        messages.success(
            request,
            "Resource deleted successfully.",
        )

        return redirect(
            "teacher_resources_list"
        )

    context = {
        "resource": resource,
    }

    return render(
        request,
        "core/teacher/resources/teacher_resource_delete.html",
        context,
    )


# =====================================================
# FORUM CRUD
# =====================================================

@login_required
def teacher_forum_list_view(request):

    forum_posts = ForumPost.objects.filter(
        author=request.user
    )

    context = {
    "posts": forum_posts,
    "form": ForumPostForm(),
    }

    return render(
        request,
        "core/teacher/forum/teacher_forum_list.html",
        context,
    )


@login_required
def teacher_forum_create_view(request):

    if request.method == "POST":

        form = ForumPostForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            post = form.save(
                commit=False
            )

            post.author = request.user
            post.save()

            messages.success(
                request,
                "Forum post created successfully.",
            )

            return redirect(
                "teacher_forum_list",
            )

    else:

        form = ForumPostForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "core/teacher/forum/teacher_forum_form.html",
        context,
    )


@login_required
def teacher_forum_detail_view(request, pk):

    forum_post = get_object_or_404(
        ForumPost,
        pk=pk,
        author=request.user,
    )

    if request.method == "POST":

        if forum_post.is_locked:

            messages.warning(
                request,
                "This thread is locked and cannot accept replies.",
            )

            return redirect(
                "teacher_forum_detail",
                pk=forum_post.pk,
            )

        reply_form = ForumReplyForm(
            request.POST,
        )

        if reply_form.is_valid():

            reply = reply_form.save(
                commit=False
            )

            reply.post = forum_post
            reply.author = request.user
            reply.save()

            messages.success(
                request,
                "Reply posted successfully.",
            )

            return redirect(
                "teacher_forum_detail",
                pk=forum_post.pk,
            )

    else:

        reply_form = ForumReplyForm()

    context = {
        "forum_post": forum_post,
        "post": forum_post,
        "reply_form": reply_form,
    }

    return render(
        request,
        "core/teacher/forum/teacher_forum_detail.html",
        context,
    )

@login_required
def teacher_forum_edit_view(request, pk):

    forum_post = get_object_or_404(
        ForumPost,
        pk=pk,
        author=request.user,
    )

    if request.method == "POST":

        form = ForumPostForm(
            request.POST,
            request.FILES,
            instance=forum_post,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Forum post updated successfully.",
            )

            return redirect(
                "teacher_forum_detail",
                pk=forum_post.pk,
            )

    else:

        form = ForumPostForm(
            instance=forum_post,
        )

    context = {
        "form": form,
        "forum_post": forum_post,
    }

    return render(
        request,
        "core/teacher/forum/teacher_forum_form.html",
        context,
    )

@login_required
def teacher_forum_delete_view(request, pk):

    forum_post = get_object_or_404(
        ForumPost,
        pk=pk,
        author=request.user,
    )

    if request.method == "POST":

        forum_post.delete()

        messages.success(
            request,
            "Forum post deleted successfully.",
        )

        return redirect(
            "teacher_forum_list"
        )

    context = {
        "forum_post": forum_post,
    }

    return render(
        request,
        "core/teacher/forum/teacher_forum_delete.html",
        context,
    )

@login_required
def class_analytics_view(request, pk):

    class_obj = get_object_or_404(
        Class,
        pk=pk,
        teacher=request.user,
    )

    students = ClassStudent.objects.filter(
        clazz=class_obj
    ).select_related("student")

    total_students = students.count()

    total_xp = sum(
        getattr(
            enrollment.student,
            "total_xp",
            0
        )
        for enrollment in students
    )

    average_xp = (
        total_xp / total_students
        if total_students > 0
        else 0
    )

    context = {
        "class_obj": class_obj,
        "students": students,
        "total_students": total_students,
        "total_xp": total_xp,
        "average_xp": round(average_xp, 1),
    }

    return render(
        request,
        "core/teacher/classes/class_analytics.html",
        context,
    )

@login_required
def student_analytics_view(
    request,
    class_pk,
    student_pk,
):

    class_obj = get_object_or_404(
        Class,
        pk=class_pk,
        teacher=request.user,
    )

    student = get_object_or_404(
        User,
        pk=student_pk,
    )

    enrollment = get_object_or_404(
        ClassStudent,
        clazz=class_obj,
        student=student,
    )

    context = {
        "class_obj": class_obj,
        "student": student,
        "enrollment": enrollment,
    }

    return render(
        request,
        "core/student/student_analytics.html",
        context,
    )
# =====================================================
# ANALYTICS
# =====================================================

@login_required
def teacher_analytics_view(request):

    classes = Class.objects.filter(
        teacher=request.user
    )

    context = {
        "classes": classes,
    }

    return render(
        request,
        "core/teacher/analytics/teacher_analytics.html",
        context,
    )