from django.shortcuts import redirect, render



def home_page_view(request):
    return render(request, "core/public/home.html")


def about_page_view(request):
    return render(request, "core/public/about.html")


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
    return render(request, "core/public/contact.html")


def wonderworld_page_view(request):
    return render(request, "core/public/wonderworld.html")


def hello(request):
    return render(request, "core/public/hello.html")