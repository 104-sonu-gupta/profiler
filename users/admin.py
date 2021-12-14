from django.contrib import admin

from .models import userProfile, Skill

# Register your models here.

@admin.register(userProfile)
class userProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['username']

admin.site.register(Skill)
