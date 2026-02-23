from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm

from django.http import HttpResponseRedirect
from .models import TeachingResource, Class

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "core/register.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    if user.role == "teacher":
        resources = TeachingResource.objects.filter(teacher=user)
        classes = Class.objects.filter(teacher=user)
        return render(request, "core/teacher_dashboard.html", {"resources": resources, "classes": classes})
    elif user.role == "school_admin":
        # Get all teachers in the same school
        teachers = User.objects.filter(role="teacher", school=user.school)
        # Collect teacher profiles, resources, and classes
        teacher_profiles = teachers
        resources = TeachingResource.objects.filter(teacher__in=teachers)
        classes = Class.objects.filter(teacher__in=teachers)
        # Example analytics: count of teachers, resources, classes
        analytics = {
            "teacher_count": teachers.count(),
            "resource_count": resources.count(),
            "class_count": classes.count(),
            # Add more analytics as needed
        }
        return render(
            request,
            "core/school_admin_dashboard.html",
            {
                "teacher_profiles": teacher_profiles,
                "resources": resources,
                "classes": classes,
                "analytics": analytics,
            },
        )
    # Add logic for other roles as needed
    return render(request, "core/dashboard.html")


# Custom login view to handle 'Remember Me'
from django.contrib.auth.views import LoginView
class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        remember = self.request.POST.get('remember')
        if not remember:
            # Session will expire when the browser closes
            self.request.session.set_expiry(0)
        else:
            # Session will persist as per SESSION_COOKIE_AGE
            self.request.session.set_expiry(None)
        return super().form_valid(form)

@login_required
def profile(request):
    user = request.user
    return render(request, "core/profile.html", {"user": user})

class CustomAuthenticationForm(CustomAuthenticationForm):
    pass
