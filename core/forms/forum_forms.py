from django import forms

from django_summernote.widgets import (
    SummernoteWidget,
)

from core.models import (
    ForumPost,
    ForumReply,
)


# =====================================================
# FORUM POST FORM
# =====================================================

class ForumPostForm(forms.ModelForm):

    class Meta:

        model = ForumPost

        fields = (
            'title',
            'description',
            'uploaded_file',
            'image',
            'allow_replies',
        )

        widgets = {

            # TITLE

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Enter post title'
                    ),
                }
            ),

            # DESCRIPTION

            'description': SummernoteWidget(),

            # FILE UPLOAD

            'uploaded_file': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            # IMAGE

            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            # ALLOW REPLIES

            'allow_replies': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

        labels = {

            'uploaded_file': (
                'Upload Supporting File'
            ),

            'image': (
                'Upload Image'
            ),

            'allow_replies': (
                'Allow replies and discussion'
            ),
        }

        help_texts = {

            'uploaded_file': (
                'Optional: PDFs, worksheets, '
                'PowerPoints, documents, etc.'
            ),

            'description': (
                'All posts are reviewed regularly '
                'for safeguarding, equality, '
                'diversity and professional '
                'conduct compliance.'
            ),
        }


# =====================================================
# FORUM REPLY FORM
# =====================================================

class ForumReplyForm(forms.ModelForm):

    class Meta:

        model = ForumReply

        fields = (
            'content',
        )

        widgets = {

            'content': SummernoteWidget(),
        }

        help_texts = {

            'content': (
                'Replies must follow community '
                'guidelines and professional '
                'conduct expectations.'
            ),
        }