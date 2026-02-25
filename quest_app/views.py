import json
import logging
import random
import re
import time
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.cache import cache

from .forms import (
    ClassForm,
    CustomAuthenticationForm,
    CustomUserCreationForm,
    ResourceCommentForm,
    TeachingResourceForm,
)
from .models import (
    Class,
    ResourceComment,
    TeachingResource,
    StudentPassword,
)

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from .models import StudentPassword
from io import BytesIO
from django.http import FileResponse, HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

# Module logger
logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        logger.info(
            "Registration POST received from %s", request.META.get("REMOTE_ADDR")
        )
        if form.is_valid():
            # Ensure we create a unique username (username isn't collected on the form)
            User = get_user_model()
            email = form.cleaned_data.get("email") or ""
            first = (form.cleaned_data.get("first_name") or "").strip()
            last = (form.cleaned_data.get("last_name") or "").strip()
            if email:
                base = email.split("@", 1)[0]
            else:
                base = (first + last) or "user"
            # sanitize base to alnum
            base = re.sub(r"[^a-z0-9]", "", base.lower()) or "user"
            username = base
            suffix = 1
            while User.objects.filter(username=username).exists():
                username = f"{base}{suffix}"
                suffix += 1

            try:
                # Build a clean user creation path to ensure the user is persisted
                User = get_user_model()
                pwd = form.cleaned_data.get("password1")
                # Collect basic fields from the form
                email = form.cleaned_data.get("email") or ""
                first = (form.cleaned_data.get("first_name") or "").strip()
                last = (form.cleaned_data.get("last_name") or "").strip()
                role = form.cleaned_data.get("role") or None

                logger.info("Creating user: email=%s username=%s", email, username)

                # Use the manager's create_user to ensure proper handling
                user = User.objects.create_user(
                    username=username, email=email, password=pwd
                )
                user.first_name = first
                user.last_name = last
                if role:
                    user.role = role

                # If the form included an uploaded avatar or other file fields, attach them
                try:
                    if request.FILES:
                        if hasattr(user, "avatar") and request.FILES.get("avatar"):
                            user.avatar = request.FILES.get("avatar")
                except Exception:
                    logger.exception(
                        "Failed to attach uploaded files for user %s", username
                    )

                user.save()
                logger.info(
                    "User created: id=%s username=%s",
                    getattr(user, "id", None),
                    username,
                )
            except IntegrityError:
                logger.warning(
                    "IntegrityError creating user username=%s email=%s", username, email
                )
                form.add_error(
                    None,
                    "A user with that username already exists. Please choose a different email or contact the admin.",
                )
                return render(request, "core/register.html", {"form": form})
            except Exception:
                logger.exception(
                    "Unexpected error during registration for username=%s email=%s",
                    username,
                    email,
                )
                form.add_error(
                    None,
                    "An unexpected error occurred. Please try again or contact support.",
                )
                return render(request, "core/register.html", {"form": form})

            # Log the user in
            login(request, user)
            # Respect the 'remember_me' choice on registration (default True)
            try:
                remember = form.cleaned_data.get("remember_me", True)
                if remember:
                    # Persistent session (will use SESSION_COOKIE_AGE)
                    request.session.set_expiry(None)
                else:
                    # Session expires on browser close
                    request.session.set_expiry(0)
            except Exception:
                pass

            # For teachers, keep a local minimal record (git-ignored file)
            try:
                if getattr(user, "role", "") == "teacher":
                    path = Path(settings.BASE_DIR) / ".saved_teachers.json"
                    records = []
                    if path.exists():
                        try:
                            records = json.loads(path.read_text(encoding="utf-8")) or []
                        except Exception:
                            records = []
                    records.append(
                        {
                            "username": user.username,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "created": datetime.utcnow().isoformat() + "Z",
                        }
                    )
                    path.write_text(json.dumps(records, indent=2), encoding="utf-8")
            except Exception:
                # don't block registration on IO error
                pass

            return redirect("dashboard")
        else:
            # Log invalid form for diagnostics (don't log sensitive fields)
            try:
                logger.warning(
                    "Registration form invalid: errors=%s", form.errors.as_json()
                )
            except Exception:
                logger.warning(
                    "Registration form invalid and could not serialize errors"
                )
    else:
        form = CustomUserCreationForm()
    return render(request, "core/register.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    if user.role == "teacher":
        resources = TeachingResource.objects.filter(teacher=user)
        classes = Class.objects.filter(teacher=user)
        return render(
            request,
            "core/teacher_dashboard.html",
            {"resources": resources, "classes": classes},
        )
    elif user.role == "school_admin":
        # Get all teachers in the same school
        teachers = get_user_model().objects.filter(role="teacher", school=user.school)
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


class CustomLoginView(LoginView):
    template_name = "core/login.html"
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        remember = self.request.POST.get("remember")
        if not remember:
            # Session will expire when the browser closes
            self.request.session.set_expiry(0)
        else:
            # Session will persist as per SESSION_COOKIE_AGE
            self.request.session.set_expiry(None)
        # Let the base class log the user in and build the normal response
        response = super().form_valid(form)
        # Log minimal debug info (never log passwords).
        try:
            hdr = (
                self.request.META.get("HTTP_X_LOGIN_DEBUG")
                or self.request.headers.get("X-Login-Debug")
                if hasattr(self.request, "headers")
                else None
            )
            uname_field = (
                self.request.POST.get("username")
                or self.request.POST.get("login")
                or ""
            )
            logger.warning(
                "Login processed: username_field_present=%s, x_login_debug=%s, path=%s",
                bool(uname_field),
                bool(hdr),
                self.request.path,
            )
            try:
                print(
                    f"LOGIN DEBUG: username_field_present={bool(uname_field)}, x_login_debug={bool(hdr)}, path={self.request.path}"
                )
            except Exception:
                pass
        except Exception:
            pass
        # If the client requested a debug JSON response (from the injected client-side helper),
        # return a small JSON payload rather than the normal redirect to aid debugging.
        try:
            if self.request.META.get("HTTP_X_LOGIN_DEBUG") == "1" or (
                hasattr(self.request, "headers")
                and self.request.headers.get("X-Login-Debug") == "1"
            ):
                # Determine where we'd redirect the user normally
                try:
                    redirect_to = self.get_success_url()
                except Exception:
                    redirect_to = "/"
                return JsonResponse({"status": "ok", "redirect": redirect_to})
        except Exception:
            pass
        try:
            user = form.get_user() if hasattr(form, "get_user") else self.request.user
            if getattr(user, "role", None) == "teacher":
                from django.shortcuts import redirect

                return redirect("dashboard")
        except Exception:
            pass
        return response

    def get_success_url(self):
        # Always send teachers to the dashboard regardless of `next`.
        try:
            user = self.request.user
            if getattr(user, "role", None) == "teacher":
                return reverse("dashboard")
        except Exception:
            pass
        return super().get_success_url()


@login_required
def profile(request):
    user = request.user
    return render(request, "core/profile.html", {"user": user})


@login_required
def class_detail(request, pk):
    cls = get_object_or_404(Class, pk=pk)
    # Only allow teachers who own the class or school_admins
    if request.user != cls.teacher and request.user.role != "school_admin":
        return redirect("teacher_dashboard")

    message = None
    created_credentials = None

    def _make_username(fname, linitial):
        base = (fname or "").strip().lower() + (linitial or "").strip().lower()
        base = "".join(ch for ch in base if ch.isalnum()) or "student"
        User = get_user_model()
        username = base
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{suffix}"
            suffix += 1
        return username

    def _make_password():
        # simple adjective+noun+number generator
        adjs = ["blue", "green", "bright", "silent", "quick", "brave", "happy", "sunny"]
        nouns = [
            "apple",
            "river",
            "mountain",
            "ocean",
            "fox",
            "panda",
            "stone",
            "ember",
        ]
        a = random.choice(adjs)
        b = random.choice(nouns)
        num = random.randint(10, 99)
        # Return two words followed by a number (e.g. "blueapple42")
        return f"{a}{b}{num}"

    if request.method == "POST":
        action = request.POST.get("action")
        User = get_user_model()

        if action == "create_student":
            fname = request.POST.get("first_name", "").strip()
            linitial = request.POST.get("last_initial", "").strip()
            if not fname or not linitial:
                message = ("error", "First name and last initial are required.")
            else:
                username = _make_username(fname, linitial)
                password = _make_password()
                user = User.objects.create_user(username=username, password=password)
                user.first_name = fname
                user.last_name = linitial
                user.role = "student"
                user.save()
                cls.students.add(user)
                created_credentials = {
                    "username": username,
                    "password": password,
                    "name": user.get_full_name() or username,
                }
                # Cache the plaintext password for teacher retrieval (no explicit TTL)
                try:
                    cache.set(f"student_pw:{user.id}", password)
                except Exception:
                    pass
                # Persist plaintext password so it remains available even if cache is cleared
                try:
                    StudentPassword.objects.update_or_create(
                        user=user, defaults={"password": password}
                    )
                except Exception:
                    pass
                message = ("success", f'Created student {created_credentials["name"]}.')

        elif action == "remove_student":
            uid = request.POST.get("user_id")
            try:
                user = User.objects.get(pk=uid)
                cls.students.remove(user)
                message = (
                    "success",
                    f"Removed {user.get_full_name() or user.username} from class.",
                )
            except Exception:
                message = ("error", "Could not remove student.")

        elif action == "delete_student":
            uid = request.POST.get("user_id")
            try:
                user = User.objects.get(pk=uid)
                user.delete()
                message = ("success", "Student account deleted.")
            except Exception:
                message = ("error", "Could not delete student.")

        elif action == "move_student":
            uid = request.POST.get("user_id")
            target = request.POST.get("target_class")
            try:
                target_cls = Class.objects.get(pk=int(target))
                user = User.objects.get(pk=uid)
                cls.students.remove(user)
                target_cls.students.add(user)
                message = (
                    "success",
                    f"Moved {user.get_full_name() or user.username} to {target_cls.name}.",
                )
            except Exception:
                message = ("error", "Could not move student.")

        elif action == "edit_student":
            uid = request.POST.get("user_id")
            new_fname = request.POST.get("first_name", "").strip()
            new_linit = request.POST.get("last_initial", "").strip()
            new_pw = request.POST.get("password", "").strip()
            try:
                user = User.objects.get(pk=uid)
                if new_fname:
                    user.first_name = new_fname
                if new_linit:
                    user.last_name = new_linit
                if new_pw:
                    user.set_password(new_pw)
                    # Cache the new plaintext password for teacher retrieval (no explicit TTL)
                    try:
                        cache.set(f"student_pw:{user.id}", new_pw)
                    except Exception:
                        pass
                    # Persist plaintext password so it survives cache eviction
                    try:
                        StudentPassword.objects.update_or_create(
                            user=user, defaults={"password": new_pw}
                        )
                    except Exception:
                        pass
                user.save()
                message = ("success", "Student updated.")
            except Exception:
                message = ("error", "Could not update student.")

        elif action == "archive_student":
            uid = request.POST.get("user_id")
            try:
                user = User.objects.get(pk=uid)
                # mark inactive instead of deleting to preserve data
                user.is_active = False
                user.save(update_fields=["is_active"])
                # remove from this class so it no longer appears in the class list
                try:
                    cls.students.remove(user)
                except Exception:
                    # non-fatal; proceed
                    pass
                message = ("success", "Student archived.")
            except Exception:
                message = ("error", "Could not archive student.")

    students = cls.students.all()
    # also supply classes that teacher owns for move target
    other_classes = Class.objects.filter(teacher=request.user).exclude(pk=cls.pk)
    return render(
        request,
        "core/class_detail.html",
        {
            "class": cls,
            "students": students,
            "message": message,
            "created_credentials": created_credentials,
            "other_classes": other_classes,
        },
    )


@login_required
def classes_list(request):
    user = request.user
    if user.role == "teacher":
        classes = Class.objects.filter(teacher=user)
    elif user.role == "school_admin":
        teachers = get_user_model().objects.filter(role="teacher", school=user.school)
        classes = Class.objects.filter(teacher__in=teachers)
    else:
        classes = Class.objects.none()
    return render(request, "core/class_list.html", {"classes": classes})


@login_required
def archived_students(request):
    """View that lists archived (inactive) student accounts relevant to the
    requesting teacher or school admin. Teachers see inactive students in their
    school; school_admins see all inactive students in their school.

    Supports POST action `restore_student` to re-enable an archived student.
    """
    user = request.user
    User = get_user_model()

    if user.role not in ("teacher", "school_admin"):
        return redirect("dashboard")

    message = None
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "restore_student":
            uid = request.POST.get("user_id")
            try:
                s = User.objects.get(pk=uid, role="student")
                # Permission: school_admin may restore any student in their school;
                # teachers may restore students in their school.
                allowed = False
                if user.role == "school_admin":
                    if getattr(user, "school", None) and user.school == getattr(s, "school", None):
                        allowed = True
                else:
                    if getattr(user, "school", None) and user.school == getattr(s, "school", None):
                        allowed = True

                if not allowed:
                    message = ("error", "Permission denied.")
                else:
                    s.is_active = True
                    s.save(update_fields=["is_active"])
                    message = ("success", f"Restored {s.get_full_name() or s.username}.")
            except Exception:
                message = ("error", "Could not restore student.")

    # List inactive students filtered by school if available
    qs = User.objects.filter(role="student", is_active=False)
    if getattr(user, "school", None):
        qs = qs.filter(school=user.school)

    students = qs.order_by("last_name", "first_name", "username")
    return render(request, "core/archived_students.html", {"students": students, "message": message})


@login_required
@require_http_methods(["POST"])
def create_student_api(request):
    """AJAX endpoint: create a student, add to class, optionally email credentials.
    Expects JSON: {"class_id": 1, "first_name": "Alice", "last_initial": "B", "email": "a@example.com", "send_email": true}
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    class_id = payload.get("class_id")
    fname = (payload.get("first_name") or "").strip()
    linit = (payload.get("last_initial") or "").strip()
    email = (payload.get("email") or "").strip() or None
    send_email_flag = bool(payload.get("send_email"))

    if not class_id or not fname or not linit:
        return JsonResponse(
            {
                "success": False,
                "error": "class_id, first_name and last_initial required",
            },
            status=400,
        )

    cls = get_object_or_404(Class, pk=int(class_id))
    # permission: teacher of class or school_admin
    if request.user != cls.teacher and request.user.role != "school_admin":
        return JsonResponse(
            {"success": False, "error": "Permission denied"}, status=403
        )

    # helper functions (same logic as in page view)
    def _make_username(fname, linitial):
        base = (fname or "").strip().lower() + (linitial or "").strip().lower()
        base = "".join(ch for ch in base if ch.isalnum()) or "student"
        User = get_user_model()
        username = base
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{suffix}"
            suffix += 1
        return username

    def _make_password():
        adjs = ["blue", "green", "bright", "silent", "quick", "brave", "happy", "sunny"]
        nouns = [
            "apple",
            "river",
            "mountain",
            "ocean",
            "fox",
            "panda",
            "stone",
            "ember",
        ]
        a = random.choice(adjs)
        b = random.choice(nouns)
        num = random.randint(10, 99)
        # Two words and a number, concatenated for readability (e.g. blueapple42)
        return f"{a}{b}{num}"

    User = get_user_model()
    username = _make_username(fname, linit)
    password = _make_password()
    user = User.objects.create_user(username=username, password=password)
    user.first_name = fname
    user.last_name = linit
    user.role = "student"
    if email:
        user.email = email
    user.save()
    cls.students.add(user)

    # email credentials if requested
    emailed = False
    if send_email_flag and email:
        try:
            subject = "Your INQ-ED student account"
            body = f"Hello {fname},\n\nAn account has been created for you on INQ-ED.\n\nUsername: {username}\nPassword: {password}\n\nPlease log in and change your password.\n\nBest regards,\nINQ-ED"
            send_mail(
                subject,
                body,
                getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
                [email],
            )
            emailed = True
        except Exception:
            # don't fail creation if email fails; include warning
            pass
    # Cache the plaintext password so teachers can retrieve it (no explicit TTL)
    try:
        cache.set(f"student_pw:{user.id}", password)
    except Exception:
        pass
    # Persist plaintext password so it remains available even if cache is cleared
    try:
        StudentPassword.objects.update_or_create(user=user, defaults={"password": password})
    except Exception:
        pass

    return JsonResponse(
        {
            "success": True,
            "id": user.id,
            "username": username,
            "password": password,
            "emailed": emailed,
        }
    )


@require_http_methods(["POST"])
def student_login_api(request):
    """Student login endpoint using name (username) + password.

    Returns JWT `access` and `refresh` on success. Enforces role == 'student'.
    Tracks failed attempts on `StudentProfile` and includes a prompt to
    contact the teacher when attempts exceed a modest threshold.
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    username = (payload.get("username") or payload.get("name") or "").strip()
    password = payload.get("password") or ""
    if not username or not password:
        return JsonResponse({"success": False, "error": "username and password required"}, status=400)

    User = get_user_model()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "Invalid credentials"}, status=401)

    # Ensure this endpoint is only for students
    if getattr(user, "role", None) != "student":
        return JsonResponse({"success": False, "error": "Not a student account"}, status=403)

    user_obj = authenticate(request, username=username, password=password)
    if user_obj is None:
        # authentication failed: increment failed_attempts on profile if present
        try:
            profile = getattr(user, "student_profile", None)
            if profile is None:
                # try to create a profile record if missing
                from .models import StudentProfile

                profile, _ = StudentProfile.objects.get_or_create(user=user, defaults={"student_id": f"S{user.id}"})
            profile.failed_attempts = (profile.failed_attempts or 0) + 1
            profile.last_failed_at = timezone.now()
            profile.save(update_fields=["failed_attempts", "last_failed_at"])
            prompt = None
            ATTEMPT_THRESHOLD = 5
            if profile.failed_attempts >= ATTEMPT_THRESHOLD:
                prompt = "Too many failed attempts — please contact your teacher."
        except Exception:
            prompt = None
        resp = {"success": False, "error": "Invalid credentials"}
        if prompt:
            resp["prompt"] = prompt
        return JsonResponse(resp, status=401)

    # Successful auth: reset failed attempts
    try:
        profile = getattr(user, "student_profile", None)
        if profile:
            profile.failed_attempts = 0
            profile.save(update_fields=["failed_attempts"])
    except Exception:
        pass

    # Issue JWT tokens
    refresh = RefreshToken.for_user(user)
    return JsonResponse(
        {
            "success": True,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"id": user.id, "username": user.username, "role": user.role},
        }
    )


@login_required
def print_student_cards(request, pk):
    """Render a print-friendly page of student login cards for a class.

    Permission: only the class teacher or school_admin can access.
    Shows username and the persisted student password (cache or `StudentPassword`).
    """
    cls = get_object_or_404(Class, pk=pk)
    # permission: teacher of class or school_admin
    if request.user != cls.teacher and request.user.role != "school_admin":
        return redirect("teacher_dashboard")

    students = cls.students.all().order_by("last_name", "first_name", "username")
    cards = []
    for s in students:
        # try cache first
        pw = None
        try:
            pw = cache.get(f"student_pw:{s.id}")
        except Exception:
            pw = None
        if not pw:
            try:
                sp = StudentPassword.objects.filter(user=s).first()
                if sp:
                    pw = sp.password
            except Exception:
                pw = None
        cards.append({"id": s.id, "name": s.get_full_name() or s.username, "username": s.username, "password": pw or ""})

    return render(request, "core/printable_student_cards.html", {"class": cls, "cards": cards})


@login_required
def print_student_cards_pdf(request, pk):
    """Generate a PDF of student login cards for bulk printing.

    Layout: 3 columns per row. Simple boxed cards with name, username and password.
    Permission: teacher of the class or school_admin.
    """
    cls = get_object_or_404(Class, pk=pk)
    if request.user != cls.teacher and request.user.role != "school_admin":
        return redirect("teacher_dashboard")

    students = cls.students.all().order_by("last_name", "first_name", "username")

    # Gather card data (username/password)
    cards = []
    for s in students:
        pw = None
        try:
            pw = cache.get(f"student_pw:{s.id}")
        except Exception:
            pw = None
        if not pw:
            try:
                sp = StudentPassword.objects.filter(user=s).first()
                if sp:
                    pw = sp.password
            except Exception:
                pw = None
        cards.append({"name": s.get_full_name() or s.username, "username": s.username, "password": pw or ""})

    # PDF layout constants
    buffer = BytesIO()
    page_w, page_h = A4
    c = canvas.Canvas(buffer, pagesize=A4)
    margin = 12 * mm
    cols = 3
    gap = 6 * mm
    usable_w = page_w - margin * 2
    card_w = (usable_w - gap * (cols - 1)) / cols
    rows = int((page_h - margin * 2 + gap) // (40 * mm))  # approximate rows per page
    card_h = (page_h - margin * 2 - gap * (rows - 1)) / rows

    x0 = margin
    y0 = page_h - margin - card_h

    col = 0
    row = 0
    for idx, card in enumerate(cards):
        x = x0 + col * (card_w + gap)
        y = y0 - row * (card_h + gap)

        # Draw box
        c.rect(x, y, card_w, card_h)

        # Text positions
        pad = 6 * mm
        tx = x + pad
        ty = y + card_h - pad - 10

        c.setFont("Helvetica-Bold", 10)
        c.drawString(tx, ty, card["name"])  # name
        c.setFont("Helvetica", 8)
        c.drawString(tx, ty - 12, f"Username: {card['username']}")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(tx, ty - 26, f"Password: {card['password']}")

        col += 1
        if col >= cols:
            col = 0
            row += 1
            if (row >= rows):
                c.showPage()
                col = 0
                row = 0

    c.save()
    buffer.seek(0)
    filename = f"{cls.name}_login_cards.pdf"
    return FileResponse(buffer, as_attachment=False, filename=filename)


@login_required
@require_http_methods(["POST"])
def email_student_card_pdf(request, class_pk, student_id):
    """Generate (or reuse cached) single-sheet PDF for a student and email it.

    POST JSON: {"to": "recipient@example.com"} — if omitted, uses student's email.
    Permission: teacher of class or school_admin.
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        payload = {}

    cls = get_object_or_404(Class, pk=class_pk)
    # permission: teacher of class or school_admin
    if request.user != cls.teacher and request.user.role != "school_admin":
        return JsonResponse({"success": False, "error": "Permission denied"}, status=403)

    try:
        student = get_user_model().objects.get(pk=int(student_id))
    except Exception:
        return JsonResponse({"success": False, "error": "Student not found"}, status=404)

    # recipient
    to_addr = (payload.get("to") or student.email or "").strip()
    if not to_addr:
        return JsonResponse({"success": False, "error": "No recipient address available"}, status=400)

    cache_key = f"student_card_pdf:{student.id}"
    pdf_bytes = None
    try:
        pdf_bytes = cache.get(cache_key)
    except Exception:
        pdf_bytes = None

    if not pdf_bytes:
        # create a small PDF (single card)
        buf = BytesIO()
        # use A6-ish size for single-sheet printable card: we'll still use A4 and center
        c = canvas.Canvas(buf, pagesize=A4)
        page_w, page_h = A4
        card_w = 90 * mm
        card_h = 60 * mm
        x = (page_w - card_w) / 2
        y = (page_h - card_h) / 2
        c.rect(x, y, card_w, card_h)
        pad = 6 * mm
        tx = x + pad
        ty = y + card_h - pad - 8
        c.setFont("Helvetica-Bold", 12)
        c.drawString(tx, ty, student.get_full_name() or student.username)
        c.setFont("Helvetica", 10)
        c.drawString(tx, ty - 14, f"Username: {student.username}")
        # try to show persisted password
        pw = None
        try:
            pw = cache.get(f"student_pw:{student.id}")
        except Exception:
            pw = None
        if not pw:
            try:
                sp = StudentPassword.objects.filter(user=student).first()
                if sp:
                    pw = sp.password
            except Exception:
                pw = None
        c.setFont("Helvetica-Bold", 11)
        c.drawString(tx, ty - 30, f"Password: {pw or ''}")
        c.showPage()
        c.save()
        buf.seek(0)
        pdf_bytes = buf.getvalue()
        # cache for 1 hour
        try:
            cache.set(cache_key, pdf_bytes, timeout=3600)
        except Exception:
            pass

    # send email with attachment
    try:
        subject = f"INQ-ED login card for {student.get_full_name() or student.username}"
        body = (
            f"Hello,\n\nAttached is the login card for {student.get_full_name() or student.username}.\n\n"
            "Please keep it secure.\n\nBest regards,\nINQ-ED"
        )
        msg = EmailMessage(subject, body, getattr(settings, "DEFAULT_FROM_EMAIL", None), [to_addr])
        filename = f"{student.username}_login_card.pdf"
        msg.attach(filename, pdf_bytes, "application/pdf")
        msg.send(fail_silently=False)
        return JsonResponse({"success": True, "emailed": True})
    except Exception as e:
        logger.exception("Failed to email student PDF: %s", e)
        return JsonResponse({"success": False, "error": "Failed to send email"}, status=500)


@login_required
@require_http_methods(["POST"])
def promote_class(request, pk):
    """Promote all students from class `pk` into a target class or a newly-created class.

    POST JSON:
      - target_class_id: (optional) existing class id to move students into
      - new_name: (optional) name for a new class to create if target not provided

    Behavior:
      - Only the class teacher or a `school_admin` may call.
      - Students' `StudentProfile.classroom` and the class ManyToMany are updated.
      - Progress and unlock state (stored in `Progress.data`) are left intact.
      - The previous class is archived by setting `is_deleted=True`.
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    cls = get_object_or_404(Class, pk=pk)
    # permission
    if request.user != cls.teacher and request.user.role != "school_admin":
        return JsonResponse({"success": False, "error": "Permission denied"}, status=403)

    target_id = payload.get("target_class_id")
    new_name = payload.get("new_name")

    if target_id:
        try:
            target = Class.objects.get(pk=int(target_id))
        except Exception:
            return JsonResponse({"success": False, "error": "Target class not found"}, status=404)
    else:
        # create a new class for promoted students
        if not new_name:
            new_name = f"{cls.name} (Next Year)"
        target = Class.objects.create(
            name=new_name,
            level=cls.level,
            subject=cls.subject,
            teacher=cls.teacher,
            school=cls.school,
        )

    # Move students: update StudentProfile.classroom if present, and Class M2M
    moved = 0
    from .models import StudentProfile

    students = list(cls.students.all())
    for s in students:
        try:
            # update ManyToMany relationships
            cls.students.remove(s)
            target.students.add(s)
            # update StudentProfile classroom FK if exists
            profile = getattr(s, "student_profile", None)
            if profile:
                profile.classroom = target
                profile.save(update_fields=["classroom"])
            moved += 1
        except Exception:
            logger.exception("Failed to move student %s during promotion", getattr(s, "id", None))

    # Archive previous class
    cls.is_deleted = True
    cls.save(update_fields=["is_deleted"])

    return JsonResponse({"success": True, "moved": moved, "target_class": target.id})


@login_required
@require_http_methods(["POST"])
def bulk_move_students(request, class_pk):
    """Move a list of students from the source class (`class_pk`) into a single
    target class (existing or newly-created). Designed for primary schools where
    the class stays the same but the teacher changes.

    POST JSON options:
      - student_ids: [1,2,3]  (required)
      - target_class_id: 42    (optional)
      - new_teacher_id: 99     (optional; used when creating a new class)
      - keep_name: true/false  (if creating new class, whether to copy name)

    Permissions: only the class teacher or a `school_admin` may perform.
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    student_ids = payload.get("student_ids") or []
    if not isinstance(student_ids, list) or not student_ids:
        return JsonResponse({"success": False, "error": "student_ids required"}, status=400)

    src = get_object_or_404(Class, pk=class_pk)
    # permission
    if request.user != src.teacher and request.user.role != "school_admin":
        return JsonResponse({"success": False, "error": "Permission denied"}, status=403)

    target_id = payload.get("target_class_id")
    new_teacher_id = payload.get("new_teacher_id")
    keep_name = bool(payload.get("keep_name", True))

    target = None
    if target_id:
        try:
            target = Class.objects.get(pk=int(target_id))
        except Exception:
            return JsonResponse({"success": False, "error": "Target class not found"}, status=404)
    else:
        # create new class; require teacher id or use source teacher
        if new_teacher_id:
            try:
                new_teacher = get_user_model().objects.get(pk=int(new_teacher_id))
            except Exception:
                return JsonResponse({"success": False, "error": "Teacher not found"}, status=404)
        else:
            new_teacher = src.teacher

        name = src.name if keep_name else f"{src.name} (New)"
        target = Class.objects.create(
            name=name,
            level=src.level,
            subject=src.subject,
            teacher=new_teacher,
            school=src.school,
        )

    moved = 0
    User = get_user_model()
    for sid in student_ids:
        try:
            s = User.objects.get(pk=int(sid))
        except Exception:
            continue
        # Ensure student belongs to source class before moving
        if not src.students.filter(pk=s.id).exists():
            continue
        try:
            src.students.remove(s)
            target.students.add(s)
            profile = getattr(s, "student_profile", None)
            if profile:
                profile.classroom = target
                profile.save(update_fields=["classroom"])
            moved += 1
        except Exception:
            logger.exception("Failed to move student %s in bulk move", s.id)

    return JsonResponse({"success": True, "moved": moved, "target_class": target.id})


@login_required
@require_http_methods(["POST"])
def generate_reset_api(request):
    """Generate a single-use signed reset token and return a one-time URL (no email required).
    POST JSON: {"user_id": 3}
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    uid = payload.get("user_id")
    if not uid:
        return JsonResponse({"success": False, "error": "user_id required"}, status=400)

    User = get_user_model()
    try:
        user = User.objects.get(pk=int(uid))
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "User not found"}, status=404)

    # permission: teacher who owns class or school_admins can generate for their students
    # to be safe, require that requesting user is teacher of a class that includes the student or a school_admin
    is_allowed = False
    if request.user.role == "school_admin":
        is_allowed = True
    else:
        # check teacher owns any class with this student
        if (
            Class.objects.filter(teacher=request.user, students=user).exists()
            or Class.objects.filter(teacher=request.user, students__id=user.id).exists()
        ):
            is_allowed = True

    if not is_allowed:
        return JsonResponse(
            {"success": False, "error": "Permission denied"}, status=403
        )

    # create signed token with max_age enforced on load; include a timestamp
    try:
        ts = int(time.time())
    except Exception:
        ts = 0
    token = dumps({"user_id": user.id, "ts": ts}, salt="student-reset")
    reset_url = request.build_absolute_uri(reverse("student_reset", args=[token]))
    return JsonResponse({"success": True, "url": reset_url})


@require_http_methods(["GET", "POST"])
def student_reset(request, token):
    """Allow setting a new password using a signed token. Token is single-use by virtue of being short-lived.
    We use `loads(..., max_age=86400)` to limit token validity to 24 hours.
    """
    # Prevent reuse of a token by marking used tokens in cache
    used_key = f"used_reset:{token}"
    try:
        if cache.get(used_key):
            return render(
                request,
                "core/student_reset.html",
                {"error": "Reset link already used."},
            )
    except Exception:
        # If cache is unavailable, continue (fails open)
        pass

    try:
        data = loads(token, salt="student-reset", max_age=86400)
    except SignatureExpired:
        return render(
            request, "core/student_reset.html", {"error": "Reset link expired."}
        )
    except BadSignature:
        return render(
            request, "core/student_reset.html", {"error": "Invalid reset link."}
        )

    uid = data.get("user_id")
    User = get_user_model()
    try:
        user = User.objects.get(pk=int(uid))
    except User.DoesNotExist:
        return render(request, "core/student_reset.html", {"error": "User not found."})

    if request.method == "POST":
        pw1 = request.POST.get("password")
        pw2 = request.POST.get("password2")
        if not pw1 or pw1 != pw2:
            return render(
                request, "core/student_reset.html", {"error": "Passwords do not match."}
            )
        user.set_password(pw1)
        user.save()
        # Mark token as used in cache for the remaining validity period
        try:
            ts = int(data.get("ts") or 0)
            elapsed = int(time.time()) - ts if ts else 0
            remaining = max(1, 86400 - elapsed)
            cache.set(used_key, True, timeout=remaining)
        except Exception:
            # If cache fails, don't block user; token may remain usable until expiry
            pass
        return render(
            request,
            "core/student_reset.html",
            {"success": "Password updated. The user can now log in."},
        )

    return render(request, "core/student_reset.html", {"token": token})


@login_required
def add_class(request):
    # Only teachers or school_admins may create classes
    if getattr(request.user, "role", None) not in ("teacher", "school_admin"):
        messages.error(request, "Permission denied.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            cls = form.save(commit=False)
            cls.teacher = request.user
            cls.save()
            messages.success(request, "Class created successfully.")
            return redirect("teacher_dashboard")
    else:
        form = ClassForm()
    return render(request, "core/add_class.html", {"form": form})


@login_required
def edit_class(request, pk):
    # Edit an existing class. Only the owning teacher or school_admin may edit.
    cls = get_object_or_404(Class, pk=pk)
    if not (request.user == cls.teacher or getattr(request.user, "role", None) == "school_admin"):
        messages.error(request, "Permission denied.")
        return redirect("class_detail", pk=pk)

    if request.method == "POST":
        form = ClassForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            messages.success(request, "Class updated successfully.")
            return redirect("class_detail", pk=pk)
    else:
        form = ClassForm(instance=cls)
    return render(request, "core/edit_class.html", {"form": form, "class": cls})


@login_required
@require_http_methods(["POST"])
def archive_class(request, pk):
    # Soft-delete (archive) a class. Only owner teacher or school_admin allowed.
    cls = get_object_or_404(Class, pk=pk)
    if not (request.user == cls.teacher or getattr(request.user, "role", None) == "school_admin"):
        messages.error(request, "Permission denied.")
        return redirect("class_detail", pk=pk)

    cls.is_deleted = True
    cls.save(update_fields=["is_deleted"])
    messages.success(request, "Class archived.")
    return redirect("classes")


@login_required
def teacher_resources(request):
    """List teacher resources and allow teachers to upload new ones."""
    user = request.user
    if user.role != "teacher" and user.role != "school_admin":
        return redirect("teacher_dashboard")

    if user.role == "school_admin":
        # show resources for all teachers in school
        teachers = get_user_model().objects.filter(role="teacher", school=user.school)
        qs = TeachingResource.objects.filter(teacher__in=teachers).order_by(
            "-uploaded_at"
        )
    else:
        qs = TeachingResource.objects.filter(teacher=user).order_by("-uploaded_at")

    # Pagination
    page = request.GET.get("page", 1)
    per_page = 6
    paginator = Paginator(qs, per_page)
    try:
        resources_page = paginator.page(page)
    except PageNotAnInteger:
        resources_page = paginator.page(1)
    except EmptyPage:
        resources_page = paginator.page(paginator.num_pages)

    form = TeachingResourceForm()
    message = None
    if request.method == "POST":
        form = TeachingResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.teacher = user
            resource.save()
            messages.success(request, "Resource uploaded.")
            return redirect("teacher_resources")
        else:
            message = ("error", "Please correct the errors below.")

    # If requesting a page fragment (load-more), render only the cards partial
    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get(
        "partial"
    ):
        return render(
            request,
            "core/_resource_cards.html",
            {"resources": resources_page, "user": user},
        )

    return render(
        request,
        "core/teacher_resources_list.html",
        {
            "resources": resources_page,
            "form": form,
            "message": message,
            "paginator": paginator,
        },
    )


@login_required
def resource_edit(request, pk):
    res = get_object_or_404(TeachingResource, pk=pk)
    if request.user != res.teacher:
        return redirect("teacher_resources")

    if request.method == "POST":
        # Only allow editing title and description for now
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        if not title:
            messages.error(request, "Title is required.")
        else:
            res.title = title
            res.description = description
            res.save()
            messages.success(request, "Resource updated.")
            return redirect("teacher_resources")

    # fallback render same resources page with anchor
    return redirect("teacher_resources")


@login_required
def resource_delete(request, pk):
    res = get_object_or_404(TeachingResource, pk=pk)
    if request.user != res.teacher:
        messages.error(request, "Permission denied.")
        return redirect("teacher_resources")
    if request.method == "POST":
        res.document.delete(save=False)
        res.delete()
        messages.success(request, "Resource deleted.")
    return redirect("teacher_resources")


@login_required
def resource_comment(request, pk):
    res = get_object_or_404(TeachingResource, pk=pk)
    if request.method != "POST":
        return redirect("teacher_resources")
    form = ResourceCommentForm(request.POST)
    if form.is_valid():
        comment_text = form.cleaned_data["comment"].strip()
        if comment_text:
            ResourceComment.objects.create(
                resource=res, author=request.user, comment=comment_text
            )
            messages.success(request, "Comment added.")
    else:
        messages.error(request, "Comment cannot be empty.")
    return redirect("teacher_resources")


@login_required
def add_class_ajax(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required"}, status=405)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        payload = request.POST
    name = (payload.get("name") or "").strip()
    school = (payload.get("school") or "").strip() or None
    level = (payload.get("level") or "").strip() or "LKS2"
    subject = (payload.get("subject") or "").strip() or None
    if not name:
        return JsonResponse({"success": False, "error": "Name required"}, status=400)
    try:
        # validate KS3/KS4 require subject
        if level in ("KS3", "KS4") and not subject:
            return JsonResponse(
                {"success": False, "error": "Subject required for KS3/KS4"}, status=400
            )
        cls = Class.objects.create(
            name=name, school=school, level=level, subject=subject, teacher=request.user
        )
        return JsonResponse({"success": True, "id": cls.id, "name": cls.name})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
def avatar_api(request):
    """Return current avatar configuration stored in session (or default)."""
    data = request.session.get("inqed_avatar")
    if not data:
        # default avatar values
        data = {
            "bodyType": "blob",
            "bodyColor": "#FF6B9D",
            "eyeType": "big_round",
            "mouthType": "happy",
            "headDecoration": "horns",
            "decorationColor": "#FFB347",
            "pattern": "solid",
            "patternColor": "#FF1493",
        }
    return JsonResponse(data)


@login_required
def avatar_save(request):
    """Save avatar config into session (simple stub, no DB changes)."""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required"}, status=405)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    # Validate keys minimally
    allowed = {
        "bodyType",
        "bodyColor",
        "eyeType",
        "mouthType",
        "headDecoration",
        "decorationColor",
        "pattern",
        "patternColor",
    }
    avatar = {k: v for k, v in payload.items() if k in allowed}
    request.session["inqed_avatar"] = avatar
    request.session.modified = True
    return JsonResponse({"success": True})


@login_required
def avatar_randomize(request):
    """Return a randomized avatar configuration and save to session."""
    # create randomized values
    bodyTypes = ["blob", "round", "tall", "wide", "pear", "bean"]
    eyeTypes = ["big_round", "small_dots", "one_eye", "sleepy", "googly", "angry"]
    mouthTypes = ["happy", "toothy", "small", "big_smile", "oh", "silly"]
    headDecor = ["none", "horns", "antennae", "spikes", "ears", "mohawk"]
    colors = ["#FF6B9D", "#FFB347", "#7BD389", "#76B4FF", "#C38DFF", "#FFD36E"]
    patterns = ["solid", "spots", "stripes", "gradient"]

    def pick(arr):
        return random.choice(arr)

    data = {
        "bodyType": pick(bodyTypes),
        "bodyColor": pick(colors),
        "eyeType": pick(eyeTypes),
        "mouthType": pick(mouthTypes),
        "headDecoration": pick(headDecor),
        "decorationColor": pick(colors),
        "pattern": pick(patterns),
        "patternColor": pick(colors),
    }
    request.session["inqed_avatar"] = data
    request.session.modified = True
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def summernote_upload(request):
    """Simple file upload endpoint used by the Summernote plugin.

    Expects a multipart/form-data POST with field `file`. Returns JSON
    {"url": "<public url>"} on success.
    """
    if not request.FILES:
        return JsonResponse({"success": False, "error": "No file provided"}, status=400)
    upload = request.FILES.get("file") or next(iter(request.FILES.values()))
    try:
        subpath = f"uploads/summernote/{int(time.time())}_{upload.name}"
        saved_path = default_storage.save(subpath, ContentFile(upload.read()))
        url = settings.MEDIA_URL + saved_path
        return JsonResponse({"success": True, "url": url})
    except Exception as e:
        logger.exception("summernote upload failed")
        return JsonResponse({"success": False, "error": "Upload failed"}, status=500)


@login_required
@require_http_methods(["POST"])
def reveal_student_password(request, pk):
    """Return cached plaintext password for a student if teacher/school_admin authorized."""
    User = get_user_model()
    try:
        student = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "User not found"}, status=404)

    # permission: teacher of any class including this student, or school_admin in same school
    allowed = False
    if request.user.role == "school_admin":
        if getattr(request.user, "school", None) and request.user.school == getattr(student, "school", None):
            allowed = True
    else:
        # teacher must own a class that contains the student
        if Class.objects.filter(teacher=request.user, students=student).exists():
            allowed = True

    if not allowed:
        return JsonResponse({"success": False, "error": "Permission denied"}, status=403)

    try:
        pw = cache.get(f"student_pw:{student.id}")
    except Exception:
        pw = None
    # If cache missed, fall back to persistent store so teachers can always retrieve
    if not pw:
        try:
            sp = StudentPassword.objects.filter(user=student).first()
            if sp:
                pw = sp.password
        except Exception:
            pw = None

    if not pw:
        return JsonResponse({"success": False, "error": "Password unavailable. Consider generating a reset link."}, status=404)

    return JsonResponse({"success": True, "password": pw})


@login_required
def profile_update(request):
    """API endpoint to update simple profile fields via AJAX.
    Expects JSON: {"field": "email", "value": "new@example.com"}
    Special-case: field == 'name' will update first_name and last_name by splitting value.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required"}, status=405)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    field = payload.get("field")
    value = payload.get("value", "")
    user = request.user

    if not field:
        return JsonResponse({"success": False, "error": "Missing field"}, status=400)

    try:
        if field == "name":
            parts = value.strip().split()
            user.first_name = parts[0] if parts else ""
            user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        elif field in ("first_name", "last_name", "role", "school", "bio"):
            setattr(user, field, value)
        elif field == "email":
            # validate email format
            try:
                validate_email(value)
            except ValidationError:
                return JsonResponse(
                    {"success": False, "error": "Invalid email address"}, status=400
                )
            # ensure email is not used by another user
            User = get_user_model()
            if User.objects.filter(email=value).exclude(pk=user.pk).exists():
                return JsonResponse(
                    {"success": False, "error": "Email already in use"}, status=400
                )
            user.email = value
        else:
            # attempt to set attribute if exists on user model
            if hasattr(user, field):
                setattr(user, field, value)
            else:
                return JsonResponse(
                    {"success": False, "error": "Field not allowed"}, status=400
                )
        user.save()
        return JsonResponse({"success": True, "field": field, "value": value})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


class CustomAuthenticationForm(CustomAuthenticationForm):
    pass
