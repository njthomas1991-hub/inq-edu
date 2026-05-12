from django import forms
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import SignupForm

from core.models import User


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username or Email',
                'autocomplete': 'username',
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'autocomplete': 'current-password',
            }
        )
    )


class CustomSignupForm(SignupForm):

    ROLE_DESCRIPTIONS = {
        'teacher': 'A teacher who creates and manages classes and students.',
        'student': 'A student who participates in classes and activities.',
        'school_admin': 'A school administrator with oversight access.',
    }

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                'class': 'role-radio'
            }
        ),
        required=True,
        label='I am a',
        initial='teacher'
    )

    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }
        )
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }
        )
    )

    school = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'School name'
            }
        )
    )

    def save(self, request):

        user = super().save(request)

        role = self.cleaned_data.get('role', 'teacher')

        if hasattr(user, 'role'):
            user.role = role

        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')

        school = self.cleaned_data.get('school', '')

        if hasattr(user, 'school'):
            user.school = school

        user.is_staff = role in ['teacher', 'school_admin']

        user.save()

        return user