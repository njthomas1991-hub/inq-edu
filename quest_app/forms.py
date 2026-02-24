from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import Class
from .models import TeachingResource
import logging
from django.core.validators import validate_email

# module logger
logger = logging.getLogger(__name__)


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
            email = (self.data.get('username') or self.data.get('login') or '').strip()
        except Exception:
            email = None
        if email:
            # Only treat the input as an email when it looks like one
            is_email = False
            try:
                if '@' in email:
                    validate_email(email)
                    is_email = True
            except Exception:
                is_email = False

            if not is_email:
                # user entered a username (no '@') -- do not attempt email->username mapping
                return super().clean()

            try:
                user = User.objects.get(email__iexact=email)
                logger.warning('Auth form: mapped email %s -> username %s', email, user.username)
                try:
                    print(f"AUTH DEBUG: mapped email {email} -> username {user.username}")
                except Exception:
                    pass
            except User.MultipleObjectsReturned:
                user = User.objects.filter(email__iexact=email).order_by('id').first()
                if user:
                    logger.warning('Auth form: multiple users with email %s, selected username %s', email, user.username)
            except User.DoesNotExist:
                user = None
                logger.warning('Auth form: no user found with email %s', email)
                try:
                    print(f"AUTH DEBUG: no user found with email {email}")
                except Exception:
                    pass
                # Provide a friendly validation error for unknown emails so the
                # user sees a clear message on the login page instead of the
                # generic authentication failure text.
                try:
                    raise forms.ValidationError('No account found for that email address. Please register or check the email entered.')
                except forms.ValidationError:
                    # Attach the error to the form's non-field errors and return early
                    self.add_error(None, 'No account found for that email address. Please register or check the email entered.')
                    return super().clean()
            if user:
                # set the username field to the found user's username
                try:
                    self.data = self.data.copy()
                    self.data['username'] = user.username
                except Exception:
                    logger.exception('Auth form: failed to set self.data username for email %s', email)
                    try:
                        print(f"AUTH DEBUG: failed to set self.data username for email {email}")
                    except Exception:
                        pass
        return super().clean()
