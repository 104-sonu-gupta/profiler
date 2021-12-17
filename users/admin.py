from django.contrib import admin
from django.db.models import fields

from .models import *

# Register your models here.

@admin.register(userProfile)
class userProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['username']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Skill._meta.fields if field.name!='description']

