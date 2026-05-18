from django import forms

from core.models import User


class ProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "display_name",
            "first_name",
            "last_name",
            "email",
            "school",
            "bio",
            "profile_image",
        ]

        widgets = {
            "display_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Display name",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email address",
                }
            ),
            "school": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "School",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Tell us about yourself",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if "profile_image" in self.fields:

            self.fields["profile_image"].widget.attrs.update(
                {
                    "class": "form-control",
                }
            )
