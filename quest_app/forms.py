from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import Class


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'school']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role", "password1", "password2")

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("email", "password")
