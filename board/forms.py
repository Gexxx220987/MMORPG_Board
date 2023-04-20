from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post, Reply


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Текст')

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'content'
        ]
        labels = {
            'category': 'Категория',
            'title': 'Название',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        labels = {
            'text': 'Текст отклика'
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'})
        }
