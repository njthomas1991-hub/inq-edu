from django import forms
from django_summernote.widgets import SummernoteWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

from core.models import TeachingResource


class TeachingResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-12'),
                css_class='g-3'
            ),
            Row(
                Column('resource_type', css_class='col-md-3'),
                Column('key_stage', css_class='col-md-3'),
                Column('subject', css_class='col-md-3'),
                Column('status', css_class='col-md-3'),
                css_class='g-3'
            ),
            Row(
                Column('visibility', css_class='col-md-6'),
                Column('featured', css_class='col-md-6'),
                css_class='g-3'
            ),
        )

    class Meta:
        model = TeachingResource

        fields = (
            'title',
            'resource_type',
            'key_stage',
            'subject',
            'status',
            'visibility',
            'featured',
        )

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Resource title'
                }
            ),

            'resource_type': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'key_stage': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Subject (optional)'
                }
            ),

            'status': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'visibility': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'featured': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }