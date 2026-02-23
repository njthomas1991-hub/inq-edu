from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import Class
from .models import TeachingResource


class TeachingResourceForm(forms.ModelForm):
    class Meta:
        model = TeachingResource
        fields = ['title', 'document', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description (optional)'}),
        }


class ResourceCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add a comment...'}), label='')


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'level', 'subject', 'school']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        level = cleaned.get('level')
        subject = cleaned.get('subject')
        # Require subject for KS3 and KS4
        if level in ('KS3', 'KS4') and not subject:
            self.add_error('subject', 'Subject is required for KS3/KS4 classes.')
        # School is required
        if not cleaned.get('school'):
            self.add_error('school', 'School is required.')
        return cleaned

class CustomUserCreationForm(UserCreationForm):
    remember_me = forms.BooleanField(required=False, initial=True, label='Remember me')

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role", "password1", "password2",)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("email", "password")
