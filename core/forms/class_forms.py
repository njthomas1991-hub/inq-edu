from django import forms
import secrets
import string

from core.models import Class, User


class CreateStudentForm(forms.Form):
    """Form for teachers to create student accounts"""

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        ),
    )

    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last name",
            }
        ),
    )

    def clean_username(self):
        """Ensure username is unique"""
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self):
        """Create a new student user with generated password"""
        username = self.cleaned_data["username"]
        first_name = self.cleaned_data.get("first_name", "")
        last_name = self.cleaned_data.get("last_name", "")

        # Generate a secure random password
        password_chars = string.ascii_letters + string.digits
        plain_password = "".join(secrets.choice(password_chars) for _ in range(12))

        # Create the user
        user = User.objects.create_user(
            username=username,
            password=plain_password,
            first_name=first_name,
            last_name=last_name,
            role="student",
            plain_password=plain_password,  # Store for display
        )

        return user


class ClassForm(forms.ModelForm):

    class Meta:
        model = Class

        fields = ["name", "year_ks", "subject", "description"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter class name",
                    "required": True,
                }
            ),
            "year_ks": forms.Select(
                choices=Class.YEAR_KS_CHOICES,
                attrs={"class": "form-select", "required": True},
            ),
            "subject": forms.Select(
                choices=Class.SUBJECT_CHOICES,
                attrs={"class": "form-select", "required": True},
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Optional description",
                }
            ),
        }


class ClassGroupEditForm(forms.ModelForm):

    class Meta:

        model = Class

        fields = [
            "name",
            "teacher",
            "is_archived",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "is_archived": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, school=None, **kwargs):

        super().__init__(*args, **kwargs)

        if school:

            self.fields["teacher"].queryset = User.objects.filter(
                school=school,
                role="teacher",
            )


class StudentSignupForm(forms.Form):

    fname = forms.CharField(
        label="First Name",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First name",
                "required": True,
            }
        ),
    )

    linitial = forms.CharField(
        label="Last Initial",
        max_length=1,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last initial",
                "required": True,
            }
        ),
    )
