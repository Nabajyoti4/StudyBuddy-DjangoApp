from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import User, Room, Message
from base.api.serializers import RoomSerializer

@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    json_data = RoomSerializer(rooms, many=True)
    return Response(json_data.data)

@api_view(['GET'])
def get_room(request, id):
    room = Room.objects.get(id=id)
    json_data = RoomSerializer(room)
    return Response(json_data.data)




