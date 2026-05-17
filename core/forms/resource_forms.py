from django import forms

from django_summernote.widgets import (
    SummernoteWidget,
)

from crispy_forms.helper import (
    FormHelper,
)

from crispy_forms.layout import (
    Layout,
    Row,
    Column,
)

from core.models import (
    TeachingResource,
)


# =====================================================
# TEACHING RESOURCE FORM
# =====================================================

class TeachingResourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_tag = False

        self.helper.layout = Layout(

            # TITLE

            Row(
                Column(
                    'title',
                    css_class='col-12'
                ),
                css_class='g-3'
            ),

            # DESCRIPTION

            Row(
                Column(
                    'description',
                    css_class='col-12'
                ),
                css_class='g-3'
            ),

            # RESOURCE SETTINGS

            Row(

                Column(
                    'resource_type',
                    css_class='col-md-3'
                ),

                Column(
                    'year_ks',
                    css_class='col-md-3'
                ),

                Column(
                    'subject',
                    css_class='col-md-3'
                ),

                Column(
                    'status',
                    css_class='col-md-3'
                ),

                css_class='g-3'
            ),

            # VISIBILITY

            Row(

                Column(
                    'visibility',
                    css_class='col-md-6'
                ),

                Column(
                    'featured',
                    css_class='col-md-6'
                ),

                css_class='g-3'
            ),

            # FILES

            Row(

                Column(
                    'uploaded_file',
                    css_class='col-md-6'
                ),

                Column(
                    'image',
                    css_class='col-md-6'
                ),

                css_class='g-3'
            ),

            # COMMENTS

            Row(

                Column(
                    'allow_comments',
                    css_class='col-12'
                ),

                css_class='g-3'
            ),
        )

    class Meta:

        model = TeachingResource

        fields = (

            # CORE

            'title',
            'description',

            # CLASSIFICATION

            'resource_type',
            'year_ks',
            'subject',

            # STATUS

            'status',
            'visibility',
            'featured',

            # FILES

            'uploaded_file',
            'image',

            # INTERACTION

            'allow_comments',
        )

        widgets = {

            # TITLE

            'title': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': (
                        'Resource title'
                    )
                }
            ),

            # DESCRIPTION

            'description': SummernoteWidget(),

            # RESOURCE TYPE

            'resource_type': forms.Select(

                attrs={
                    'class': 'form-select'
                }
            ),

            # YEAR GROUP

            'year_ks': forms.Select(

                attrs={
                    'class': 'form-select'
                }
            ),

            # SUBJECT

            'subject': forms.TextInput(

                attrs={

                    'class': 'form-control',

                    'placeholder': (
                        'Subject'
                    )
                }
            ),

            # STATUS

            'status': forms.Select(

                attrs={
                    'class': 'form-select'
                }
            ),

            # VISIBILITY

            'visibility': forms.Select(

                attrs={
                    'class': 'form-select'
                }
            ),

            # FEATURED

            'featured': forms.CheckboxInput(

                attrs={
                    'class': 'form-check-input'
                }
            ),

            # FILE

            'uploaded_file': forms.ClearableFileInput(

                attrs={
                    'class': 'form-control'
                }
            ),

            # IMAGE

            'image': forms.ClearableFileInput(

                attrs={
                    'class': 'form-control'
                }
            ),

            # COMMENTS

            'allow_comments': forms.CheckboxInput(

                attrs={
                    'class': 'form-check-input'
                }
            ),
        }

        labels = {

            'uploaded_file': (
                'Upload Resource File'
            ),

            'image': (
                'Upload Cover Image'
            ),

            'allow_comments': (
                'Allow comments and discussion'
            ),
        }

        help_texts = {

            'description': (

                'All uploaded resources are '
                'reviewed regularly for '
                'safeguarding, equality, '
                'diversity, accessibility and '
                'professional conduct compliance.'
            ),

            'uploaded_file': (

                'Optional: PDF, worksheet, '
                'PowerPoint, Word document, '
                'ZIP archive, etc.'
            ),
        }