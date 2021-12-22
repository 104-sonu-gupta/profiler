from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review

from api import serializers

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRoutes(request):
    routes = [
        {'GET' : 'api/projects'},
        {'GET' : 'api/projects/id'},
 
        {'POST' : 'api/projects/id/vote'},
        {'POST' : 'api/users/token'},
        {'POST' : 'api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    # simply passing this queryset will not work  
    all_projects = Project.objects.all()   

    # Turn queryset to json datatype, many = False refers to all and True for a single object
    serializer = ProjectSerializer(all_projects, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, id):
    project = Project.objects.get(pk=id)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def voteProject(request, id):
    project =  Project.objects.get(pk=id)
    user = request.user.profile
    data = request.data

    # if user exists then it will check if already voted else it create a users and vote  
    review, create = Review.objects.get_or_create(  
        owner = user, 
        project = project
    )

    review.value = data['value']
    review.save()
    project.updateVote

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)