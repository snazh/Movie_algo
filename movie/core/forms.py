from django import forms

from .models import *


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'name': "review",
                'id': "review",
                'cols': "100",
                'rows': "4",
                'style': "resize: none;"
            })
        }

