from .models import *
from django.db.models import Q

def SearchProject(request):
    search_query = request.GET.get('search_query') or ''
    tags = Tag.objects.filter(name__icontains = search_query)
    project = Project.objects.distinct().filter(
        Q(title__icontains = search_query) |
        # Q(description__icontains = search_query) |
        # Q(tags__name__icontains = search_query) |         # method 1
        Q(tags__in = tags) |                                # method 2
        Q(owner__name__icontains = search_query)            # parent 

    ).order_by('-created')

    return project, search_query