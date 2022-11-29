from rest_framework.decorators import api_view , permission_classes
# permission_classes - veq authenticated users munden me i pa
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response

from .serializers import ProjectSerializer
from projects.models import Project
"""
@api_view(['']) perdoret per function based views
APIView - perdoret per class based views
"""

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'/api/projects'}, # returns a list of projects objects
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        # class based views for tokens
        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    # serializing data
    #varName = SerializedClass(queryset , many=True - per shum  , False-per 1)
    serializer = ProjectSerializer(projects,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getProject(request , pk):
    project = Project.objects.get(id=pk)
    # serializing data
    serializer = ProjectSerializer(project,many=False)

    return Response(serializer.data)


