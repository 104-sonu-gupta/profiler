from django.contrib import admin
from django.db import models
from .models import *
# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'title','created']
    

    class Meta:
        model = Project 


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'project', 'body','value', 'created']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created']

