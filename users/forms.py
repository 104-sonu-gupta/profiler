from django.forms import ModelForm, widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': "input input--text", 'placeholder': 'Enter username'}),
            'first_name': forms.TextInput(attrs={'class': "input input--text", 'placeholder': 'e.g., Ivan'}),
            'last_name': forms.TextInput(attrs={'class': "input input--text", 'placeholder': 'e.g., Sharma'}),
            'email': forms.EmailInput(attrs={'class': "input input--text", 'placeholder': 'e.g., ivan@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update(
            {'class': 'input input--password', 'placeholder': 'Enter password '})
        self.fields['password2'].widget.attrs.update(
            {'class': 'input input--password', 'placeholder': 'Enter password '})

    #     for key, value in self.fields.items():
    #         value.widget.attrs.update({'class': 'input'})


class userProfileForm(ModelForm):

    class Meta:
        model = userProfile
        fields = [
            'name',
            # 'username',
            'email',
            'location',
            'headline', 
            'bio', 
            'profile_pic', 
            'social_github', 
            'social_twitter', 
            'social_linkedin', 
            'social_youtube', 
            'social_website', 
        ]

    def __init__(self, *args, **kwargs):
        super(userProfileForm, self).__init__(*args, **kwargs)

        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input input--text'})

        # self.fields['social_github'].widget.attrs.update({'class': 'input input--url', 'placeholder': 'Enter URL '})



class SkillForm(ModelForm):
    
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': "input", 'placeholder': 'Enter skill name'}),
            'description': forms.Textarea(attrs={'class': "input", 'placeholder': 'Enter description (if any)'}),
        }

class MessageForm(ModelForm):
    
    class Meta:
        model = Message
        fields = ['name', 'email' , 'title', 'body']
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        for key, value in self.fields.items():  
            value.widget.attrs.update({'class': 'input input--text'})
