from django.db import models
from users.models import userProfile
import uuid
# Create your models here.

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(userProfile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(null = True, blank = True, default = 'default.jpg')
    demo_link = models.CharField(max_length=2000, blank=True, null=True)
    source_link = models.CharField(max_length=2000, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    vote_count = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    
    
    
    tags = models.ManyToManyField('Tag', blank=True)    # 'Tag' for reference b/c tag should be defined aboove Project

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    #  owner = 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)

    VOTE_TYPE = [
        ('up', 'Up Vote'),
        ('dn', 'Down Vote'),
    ]

    value = models.CharField(max_length=2, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.value



class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

