from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role", "password1", "password2")

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("email", "password")
