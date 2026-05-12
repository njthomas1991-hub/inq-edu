from django import forms

from core.models import Class, User


class ClassForm(forms.ModelForm):

    class Meta:
        model = Class

        fields = [
            'name',
            'year_ks',
            'subject',
            'description'
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter class name',
                    'required': True
                }
            ),

            'year_ks': forms.Select(
                choices=Class.KEY_STAGE_CHOICES,
                attrs={
                    'class': 'form-select',
                    'required': True
                }
            ),

            'subject': forms.Select(
                attrs={
                    'class': 'form-select',
                    'required': True
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Optional description'
                }
            ),
        }


class StudentSignupForm(forms.Form):

    fname = forms.CharField(
        label='First Name',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First name',
                'required': True
            }
        )
    )

    linitial = forms.CharField(
        label='Last Initial',
        max_length=1,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last initial',
                'required': True
            }
        )
    )