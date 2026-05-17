import random

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
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
)

from core.forms.resource_forms import (
    TeachingResourceForm,
)

from core.forms.forum_forms import (
    ForumPostForm,
)


# =====================================================
# HELPERS
# =====================================================

def teacher_required(user):

    return (
        user.is_authenticated
        and user.role in ["teacher", "school_admin"]
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
        last_name[0].lower()
        if last_name else ""
    )

    username = base

    counter = 1

    while User.objects.filter(username=username).exists():

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

    classroom = get_object_or_404(
        Class,
        pk=pk,
        teacher=request.user,
    )

    students = ClassStudent.objects.filter(
        clazz=classroom
    ).select_related("student")

    new_student = request.session.pop(
        "new_student",
        None,
    )

    context = {
        "classroom": classroom,
        "students": students,
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

            classroom = form.save(commit=False)
            classroom.teacher = request.user
            classroom.save()

            messages.success(
                request,
                "Class created successfully."
            )

            return redirect("teacher_classes")

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
                "Class updated successfully."
            )

            return redirect("teacher_classes")

    else:

        form = ClassForm(instance=classroom)

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
            "Class deleted successfully."
        )

        return redirect("teacher_classes")

    context = {
        "classroom": classroom,
    }

    return render(
        request,
        "core/teacher/classes/class_delete.html",
        context,
    )

@login_required
def add_student_to_class_view(request, pk):

    teacher_class = get_object_or_404(
        Class,
        pk=pk,
        teacher=request.user,
    )

    generated_credentials = None

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

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
            "Student created successfully."
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