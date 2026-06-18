from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render


def home_page_view(request):
    return render(request, "core/public/home.html")


def about_page_view(request):
    return render(request, "core/public/about.html")


@login_required
def kindlewick_page_view(request):

    return render(request, "core/public/kindlewick.html")


def questopia_page_view(request):
    return render(request, "core/public/questopia.html")


def pricing_page_view(request):
    return render(request, "core/public/pricing.html")


def teacher_hub_view(request):

    if request.user.is_authenticated:

        if request.user.role == "teacher":
            return redirect("teacher_dashboard")

        elif request.user.role == "school_admin":
            return redirect("school_admin_dashboard")

        elif request.user.role == "student":
            return redirect("student_dashboard")

    return render(request, "core/public/teacher_hub.html")


def contact_page_view(request):
    if request.method == "POST":
        first_name = (request.POST.get("first_name") or "").strip()
        last_name = (request.POST.get("last_name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        subject = (request.POST.get("subject") or "").strip()
        message = (request.POST.get("message") or "").strip()

        if first_name and last_name and email and subject and message:
            messages.success(
                request,
                "Thanks for getting in touch. We’ll review your message soon.",
            )
            return redirect("contact")

        messages.error(request, "Please complete every required field.")

    return render(request, "core/public/contact.html")


def wonderworld_page_view(request):
    return render(request, "core/public/wonderworld.html")


def hello(request):
    return render(request, "core/public/hello.html")
