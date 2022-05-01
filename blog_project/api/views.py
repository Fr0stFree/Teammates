from rest_framework.decorators import api_view
from rest_framework.response import Response

from rooms.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])
def getRequest(request):
    return Response({'fuck you': 'slave'})


@api_view(['GET'])
def getRooms(request):
    serializer = RoomSerializer(Room.objects.all(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    serializer = RoomSerializer(Room.objects.get(pk=pk), many=False)
    return Response(serializer.data)
