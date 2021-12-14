from django.db import models
from django.forms import ModelForm, widgets
from django import forms            
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email', 'password1', 'password2']
        
        widgets = { 
            'username'  : forms.TextInput(attrs={'class': "input input--text", 'placeholder':'Enter username'}),
            'first_name': forms.TextInput(attrs={'class': "input input--text", 'placeholder':'e.g., Ivan'}),
            'last_name' : forms.TextInput(attrs={'class': "input input--text", 'placeholder':'e.g., Sharma'}),
            'email'     : forms.EmailInput(attrs={'class': "input input--text", 'placeholder':'e.g., ivan@example.com'}),
        }

        

    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class' : 'input input--password', 'placeholder' : 'Enter password '})
        self.fields['password2'].widget.attrs.update({'class' : 'input input--password', 'placeholder' : 'Enter password '})
    
    
    #     for key, value in self.fields.items(): 
    #         value.widget.attrs.update({'class': 'input'})