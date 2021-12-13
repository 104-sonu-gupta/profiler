from django.contrib import admin

from .models import userProfile, Skill

# Register your models here.

admin.site.register(userProfile)
admin.site.register(Skill)
