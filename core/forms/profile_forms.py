from django import forms
from core.models import User


class ProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "display_name",
            "email",
            "school",
            "avatar",
        ]

        widgets = {
            "display_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "school": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }