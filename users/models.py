from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.


class userProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username  = models.CharField(max_length=255, null=True, blank=True)
    location  = models.CharField(max_length=255, null=True, blank=True)
    name  = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    headline = models.CharField(max_length=255,null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to = 'profiles/', default = 'profiles/userDefault.png')
    social_github = models.CharField(max_length=255, null=True, blank=True)
    social_twitter = models.CharField(max_length=255, null=True, blank=True)
    social_linkedin = models.CharField(max_length=255, null=True, blank=True)
    social_youtube = models.CharField(max_length=255, null=True, blank=True)
    social_website = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name =("userProfile")
        verbose_name_plural = ("userProfiles")

    def __str__(self):
        return self.username

    
class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(userProfile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
     
    # setting null because if sender delete hi account then receiver should have the message intact
    sender = models.ForeignKey(userProfile, on_delete=models.SET_NULL, null=True, blank=True) 
    
    # we have to add related name in one of these because 2 foreign keys are not allowed
    reciever = models.ForeignKey(userProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    read_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['is_read', '-created']