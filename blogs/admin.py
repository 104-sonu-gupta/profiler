from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(ModelAdmin):
    read_only_fields = ['author']
    list_display = ['title', 'author', 'created_on', 'updated_on']
    ordering = ['title']
