from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from allauth.account.forms import LoginForm as AllauthLoginForm, SignupForm

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from allauth.account.forms import LoginForm as AllauthLoginForm, SignupForm

from core.models import User, School


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username or Email",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )


class CustomAllauthLoginForm(AllauthLoginForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if "login" in self.fields:
            self.fields["login"].label = "Email"
            self.fields["login"].widget = forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                    "autocomplete": "email",
                }
            )

        if "password" in self.fields:
            self.fields["password"].widget = forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Password",
                    "autocomplete": "current-password",
                }
            )


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if "old_password" in self.fields:
            self.fields["old_password"].widget = forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Current password",
                    "autocomplete": "current-password",
                }
            )

        if "new_password1" in self.fields:
            self.fields["new_password1"].widget = forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "New password",
                    "autocomplete": "new-password",
                }
            )

        if "new_password2" in self.fields:
            self.fields["new_password2"].widget = forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Confirm new password",
                    "autocomplete": "new-password",
                }
            )


class CustomSignupForm(SignupForm):

    ROLE_DESCRIPTIONS = {
        "teacher": "A teacher who creates and manages classes and students.",
        "student": "A student who participates in classes and activities.",
        "school_admin": "A school administrator with oversight access.",
    }

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "role-radio"}),
        required=True,
        label="I am a",
        initial="teacher",
    )

    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First name"}
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last name"}
        ),
    )

    username = forms.CharField(required=False, widget=forms.HiddenInput())

    school = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "School name"}
        ),
    )


def save(self, request):

    email = self.cleaned_data.get("email", "").strip()

    base_username = email.split("@")[0]
    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    self.cleaned_data["username"] = username

    user = super().save(request)

    user.username = username

    role = self.cleaned_data.get("role", "teacher")
    user.role = role

    user.first_name = self.cleaned_data.get("first_name", "")
    user.last_name = self.cleaned_data.get("last_name", "")

    school_name = self.cleaned_data.get("school", "").strip()

    if school_name:
        from core.models import School

        school, _ = School.objects.get_or_create(name=school_name)

        user.school = school

    user.is_staff = role in ["teacher", "school_admin"]

    user.save()

    return user


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username or Email",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )


class CustomAllauthLoginForm(AllauthLoginForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if "login" in self.fields:
            self.fields["login"].label = "Email"
            self.fields["login"].widget = forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                    "autocomplete": "email",
                }
            )

        if "password" in self.fields:
            self.fields["password"].widget = forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Password",
                    "autocomplete": "current-password",
                }
            )


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if "old_password" in self.fields:
            self.fields["old_password"].widget = forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Current password",
                    "autocomplete": "current-password",
                }
            )

        if "new_password1" in self.fields:
            self.fields["new_password1"].widget = forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "New password",
                    "autocomplete": "new-password",
                }
            )

        if "new_password2" in self.fields:
            self.fields["new_password2"].widget = forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Confirm new password",
                    "autocomplete": "new-password",
                }
            )


class CustomSignupForm(SignupForm):

    ROLE_DESCRIPTIONS = {
        "teacher": "A teacher who creates and manages classes and students.",
        "student": "A student who participates in classes and activities.",
        "school_admin": "A school administrator with oversight access.",
    }

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "role-radio"}),
        required=True,
        label="I am a",
        initial="teacher",
    )

    first_name = forms.CharField(
        max_length=150,
        required=False,
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
    )

    school = forms.CharField(
        max_length=255,
        required=False,
    )

    def save(self, request):

        email = self.cleaned_data.get("email")

        base_username = email.split("@")[0]
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        self.cleaned_data["username"] = username

        user = super().save(request)

        user.username = username

        role = self.cleaned_data.get("role", "teacher")
        user.role = role

        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")

        school_name = self.cleaned_data.get("school", "").strip()

        if school_name:
            from core.models import School

            school, _ = School.objects.get_or_create(name=school_name)

            user.school = school

        user.is_staff = role in ["teacher", "school_admin"]

        user.save()

        return user

    def get_success_url(self, request):

        user = request.user

        if user.role == "teacher":
            return "/teacher/"

        if user.role == "student":
            return "/student/"

        if user.role == "school_admin":
            return "/school-admin/"

        return "/"
