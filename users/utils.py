from .models import *
from django.db.models import Q

def SearchDeveloper(request):
    search_query = request.GET.get('search_query') or ''
    skills = Skill.objects.filter(name__icontains = search_query)
    profiles = userProfile.objects.distinct().filter(       # distinct for skills
        Q(name__icontains = search_query) |     
        Q(headline__icontains = search_query) |
        Q(skill__in = skills)
    )

    return profiles, search_query