from django.db import models
from django.forms import ModelForm, widgets
from django import forms
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        exclude = ['vote_count', 'vote_ratio', 'author']

        # widgets = {
        #     'tags': forms.CheckboxSelectMultiple(),
        #     'title': forms.TextInput(attrs={'class': "input", 'placeholder': 'Enter title'}),
        # }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input input--text'})