from django.db import models
from users.models import userProfile
import uuid
# Create your models here.


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(userProfile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, blank=True, null=True)
    source_link = models.CharField(max_length=2000, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    vote_count = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True)# 'Tag' for reference b/c tag must be defined above Project

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_count', '-created']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            # if project dont have an image then display the default image or you can leave it empty
            url = 'http://127.0.0.1:8000/img/default.jpg'
        return url

    
    # so that we dont need to query it as a function in project view
    @property                   
    def updateVote(self):
        reviewsCount = self.review_set.all()
        upVotes = reviewsCount.filter(value='up').count()
        totalVotes = reviewsCount.count()
        self.vote_ratio = (upVotes / totalVotes) * 100
        self.vote_count = totalVotes
        self.save()

    # to return all the profiles / users who have voted curr project
    # I did this using user.is_autheniticated, we can also do it like below
    # @property
    # def reviewers(self):                                         # ensure that it is a simple list
    #     queryset = self.review_set.all().values_list('owner__id', flat=True)
    #     return queryset

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(userProfile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)

    VOTE_TYPE = [
        ('up', 'Up Vote'),
        ('dn', 'Down Vote'),
    ]

    value = models.CharField(max_length=2, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    # we want to ensure that a particular user can only write one review for a particular project
    # so basically we want to combine owner and project as a single unique contraint

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self) -> str:
        return self.value


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


