from django.db.models.query_utils import Q
from django.shortcuts import render

from projects.models import Project
from .models import userProfile, Skill
# Create your views here.

def profiles(request):
    queryset = userProfile.objects.all()
    # skill = Skill.objects.get

    context = {
        'profiles' : queryset
    }

    return render(request, 'profiles.html', context)

def individualprofile(request, id):
    profile = userProfile.objects.get(pk = id)

    topSkills = profile.skill_set.exclude(description__exact = '')
    otherSkills = profile.skill_set.filter(description='')

    projects = Project.objects.filter(owner = profile).order_by('-created')     # extract and order by latest project of user

    # OR we could use {% for project in profile.project_set.all %}  in HTML Template


    context = {

        'profile' : profile,
        'topSkills' : topSkills,
        'otherSkills' : otherSkills,
        'projects' : projects, 
        
    }

    return render(request, 'profile.html', context)