from django.db.models import fields
from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import userProfile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # exclude = ['project']

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)

    # To extract reviews for each project 
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        # fields = ['id', 'title', 'owner', 'vote_count', 'vote_ratio', 'tags']
        fields = '__all__'

    # always use get_<serialize method field name>
    def get_reviews(self, project):
        reviews = project.review_set.all()
        serializer = ReviewSerializer(reviews, many = True)
        return serializer.data