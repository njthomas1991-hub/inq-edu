
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import TeachingResource, Class
from django.http import JsonResponse
from django.contrib import messages
from .forms import ClassForm
import random
import json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

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


@login_required
def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            cls = form.save(commit=False)
            cls.teacher = request.user
            cls.save()
            messages.success(request, 'Class created successfully.')
            return redirect('teacher_dashboard')
    else:
        form = ClassForm()
    return render(request, 'core/add_class.html', {'form': form})


@login_required
def add_class_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        payload = request.POST
    name = (payload.get('name') or '').strip()
    school = (payload.get('school') or '').strip() or None
    level = (payload.get('level') or '').strip() or 'LKS2'
    subject = (payload.get('subject') or '').strip() or None
    if not name:
        return JsonResponse({'success': False, 'error': 'Name required'}, status=400)
    try:
        # validate KS3/KS4 require subject
        if level in ('KS3','KS4') and not subject:
            return JsonResponse({'success': False, 'error': 'Subject required for KS3/KS4'}, status=400)
        cls = Class.objects.create(name=name, school=school, level=level, subject=subject, teacher=request.user)
        return JsonResponse({'success': True, 'id': cls.id, 'name': cls.name})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def avatar_api(request):
    """Return current avatar configuration stored in session (or default)."""
    data = request.session.get('inqed_avatar')
    if not data:
        # default avatar values
        data = {
            'bodyType': 'blob',
            'bodyColor': '#FF6B9D',
            'eyeType': 'big_round',
            'mouthType': 'happy',
            'headDecoration': 'horns',
            'decorationColor': '#FFB347',
            'pattern': 'solid',
            'patternColor': '#FF1493'
        }
    return JsonResponse(data)


@login_required
def avatar_save(request):
    """Save avatar config into session (simple stub, no DB changes)."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    # Validate keys minimally
    allowed = {'bodyType','bodyColor','eyeType','mouthType','headDecoration','decorationColor','pattern','patternColor'}
    avatar = {k: v for k, v in payload.items() if k in allowed}
    request.session['inqed_avatar'] = avatar
    request.session.modified = True
    return JsonResponse({'success': True})


@login_required
def avatar_randomize(request):
    """Return a randomized avatar configuration and save to session."""
    # create randomized values
    bodyTypes = ['blob','round','tall','wide','pear','bean']
    eyeTypes = ['big_round','small_dots','one_eye','sleepy','googly','angry']
    mouthTypes = ['happy','toothy','small','big_smile','oh','silly']
    headDecor = ['none','horns','antennae','spikes','ears','mohawk']
    colors = ['#FF6B9D','#FFB347','#7BD389','#76B4FF','#C38DFF','#FFD36E']
    patterns = ['solid','spots','stripes','gradient']

    pick = lambda arr: random.choice(arr)
    data = {
        'bodyType': pick(bodyTypes),
        'bodyColor': pick(colors),
        'eyeType': pick(eyeTypes),
        'mouthType': pick(mouthTypes),
        'headDecoration': pick(headDecor),
        'decorationColor': pick(colors),
        'pattern': pick(patterns),
        'patternColor': pick(colors),
    }
    request.session['inqed_avatar'] = data
    request.session.modified = True
    return JsonResponse(data)


@login_required
def profile_update(request):
    """API endpoint to update simple profile fields via AJAX.
    Expects JSON: {"field": "email", "value": "new@example.com"}
    Special-case: field == 'name' will update first_name and last_name by splitting value.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    field = payload.get('field')
    value = payload.get('value', '')
    user = request.user

    if not field:
        return JsonResponse({'success': False, 'error': 'Missing field'}, status=400)

    try:
        if field == 'name':
            parts = value.strip().split()
            user.first_name = parts[0] if parts else ''
            user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        elif field in ('first_name', 'last_name', 'role', 'school', 'bio'):
            setattr(user, field, value)
        elif field == 'email':
            # validate email format
            try:
                validate_email(value)
            except ValidationError:
                return JsonResponse({'success': False, 'error': 'Invalid email address'}, status=400)
            # ensure email is not used by another user
            User = get_user_model()
            if User.objects.filter(email=value).exclude(pk=user.pk).exists():
                return JsonResponse({'success': False, 'error': 'Email already in use'}, status=400)
            user.email = value
        else:
            # attempt to set attribute if exists on user model
            if hasattr(user, field):
                setattr(user, field, value)
            else:
                return JsonResponse({'success': False, 'error': 'Field not allowed'}, status=400)
        user.save()
        return JsonResponse({'success': True, 'field': field, 'value': value})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

class CustomAuthenticationForm(CustomAuthenticationForm):
    pass
