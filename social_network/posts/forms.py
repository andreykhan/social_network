from django import forms

from .models import Comment, Post


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
