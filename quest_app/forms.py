import logging

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import validate_email

from .models import Class, TeachingResource, User

# module logger
logger = logging.getLogger(__name__)


class TeachingResourceForm(forms.ModelForm):
    class Meta:
        model = TeachingResource
        fields = ["title", "document", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Resource title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Short description (optional)",
                }
            ),
        }


class ResourceCommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Add a comment...",
            }
        ),
        label="",
    )


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ["name", "level", "subject", "school"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "school": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        level = cleaned.get("level")
        subject = cleaned.get("subject")
        # Require subject for KS3 and KS4
        if level in ("KS3", "KS4") and not subject:
            self.add_error("subject", "Subject is required for KS3/KS4 classes.")
        # School is required
        if not cleaned.get("school"):
            self.add_error("school", "School is required.")
        return cleaned


class CustomUserCreationForm(UserCreationForm):
    remember_me = forms.BooleanField(required=False, initial=True, label="Remember me")

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "role",
            "password1",
            "password2",
        )


class CustomAuthenticationForm(AuthenticationForm):
    # Allow user to enter either email or username; map email->username when possible
    username = forms.CharField(label="Email or Username")

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        # Map entered email to the user's username so AuthenticationForm
        # and the authentication backend can authenticate correctly.
        # Read the raw POST data for the username field (may be an email).
        email = None
        try:
            # self.data may be a QueryDict
            email = (self.data.get("username") or self.data.get("login") or "").strip()
        except Exception:
            email = None
        if email:
            # Only treat the input as an email when it looks like one
            is_email = False
            try:
                if "@" in email:
                    validate_email(email)
                    is_email = True
            except Exception:
                is_email = False

            if not is_email:
                # user entered a username (no '@') -- do not attempt email->username mapping
                return super().clean()

            try:
                user = User.objects.get(email__iexact=email)
                logger.warning(
                    "Auth form: found user for email %s (username=%s)",
                    email,
                    user.username,
                )
            except User.MultipleObjectsReturned:
                user = User.objects.filter(email__iexact=email).order_by("id").first()
                if user:
                    logger.warning(
                        "Auth form: multiple users with email %s, selected id=%s username=%s",
                        email,
                        user.id,
                        user.username,
                    )
            except User.DoesNotExist:
                user = None
                logger.warning("Auth form: no user found with email %s", email)
                try:
                    print(f"AUTH DEBUG: no user found with email {email}")
                except Exception:
                    pass
                # Friendly non-field error
                self.add_error(
                    None,
                    "No account found for that email address. Please register or check the email entered.",
                )
                return super().clean()

            if user:
                # If the found user is a student, require username login
                if getattr(user, "role", None) == "student":
                    self.add_error(
                        None,
                        "Students must log in using their username (teacher-provided credentials).",
                    )
                    return super().clean()

                # If the found user has a username, map email->username and let
                # the base AuthenticationForm handle authentication normally.
                if user.username:
                    try:
                        self.data = self.data.copy()
                        self.data["username"] = user.username
                    except Exception:
                        logger.exception(
                            "Auth form: failed to set self.data username for email %s",
                            email,
                        )
                else:
                    # No username stored for this account (legacy issue). Fall
                    # back to checking the password directly and mark the user
                    # as authenticated so login() will succeed.
                    pwd = (self.data.get("password") or "").strip()
                    if not pwd:
                        self.add_error(None, "Please enter your password.")
                        return super().clean()
                    try:
                        if user.check_password(pwd):
                            # Set the internal user cache and backend so that
                            # LoginView.login will accept this user.
                            self.user_cache = user
                            user.backend = "django.contrib.auth.backends.ModelBackend"
                            # Populate cleaned_data so form is considered valid
                            self.cleaned_data = {
                                "username": user.username or "",
                                "password": pwd,
                            }
                            return self.cleaned_data
                        else:
                            # Wrong password for the email provided
                            self.add_error(
                                None, "Please enter a correct email and password."
                            )
                            return super().clean()
                    except Exception:
                        logger.exception(
                            "Auth form: error checking password for email %s", email
                        )
                        self.add_error(None, "Authentication error. Please try again.")
                        return super().clean()
        return super().clean()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure form fields render with Bootstrap form-control where available.
        for fname in ("login", "username", "password"):
            if fname in self.fields:
                widget = self.fields[fname].widget
                existing = widget.attrs.get("class", "")
                classes = (existing + " form-control").strip()
                widget.attrs["class"] = classes
