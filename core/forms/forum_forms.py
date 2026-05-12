from django import forms
from django_summernote.widgets import SummernoteWidget
from core.models import ForumPost, ForumReply


class ForumPostForm(forms.ModelForm):

    class Meta:

        model = ForumPost

        fields = (
            'title',
            'image',
            'content'
        )

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'content': SummernoteWidget(),
        }


class ForumReplyForm(forms.ModelForm):

    class Meta:

        model = ForumReply

        fields = ('content',)

        widgets = {
            'content': SummernoteWidget(),
        }