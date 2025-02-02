from django.db import models
from tags.models import Tag
from users.models import userProfile
import uuid
from ckeditor.fields import RichTextField

# Create your models here.


STATUS_CHOICES = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(userProfile, on_delete= models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, unique=True)
    content = RichTextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to = 'posts/', default='posts/default.jpg')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    vote_count = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-updated_on']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
