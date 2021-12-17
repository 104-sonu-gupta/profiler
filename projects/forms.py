from django.db import models
from django.db.models import fields
from django.forms import ModelForm, widgets
from django import forms            # for customizing classes and fields of form

from .models import Project, Review

class ProjectForm(ModelForm):
    
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['vote_count', 'vote_ratio', 'owner']
        # OR this ↓↓ same thing bas above me likhna kam padega
        # fields = ['title', 'description', 'demo_link', 'source_link','featured_image', 'tags']

        # ↓ -> for customizing fields of form we use widgets or directly use Javascript for adding classes here
        
        widgets = {
            'tags'  : forms.CheckboxSelectMultiple(),               # so now tick marks will be displayed
            'title' : forms.TextInput(attrs={'class': "input", 'placeholder':'Enter title'}),   # Method 1 for adding class and other details
        }

    def __init__(self, *args, **kwargs):                                                        # Method 2 for adding class and other details
        super(ProjectForm, self).__init__(*args, **kwargs)

        for key, value in self.fields.items():                      # adding same class to all fields 
            value.widget.attrs.update({'class': 'input'})
        
        # self.fields['demo_link'].widget.attrs.update({'class' : 'input', 'placeholder' : 'Enter link'})       individual field update


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment to your vote',
        }
        widgets = {
            'value'  : forms.Select(attrs={'class': "input"}),
            'body' : forms.Textarea(attrs={'class': "input  input--text", 'placeholder':'Enter review'}),
        }

 
