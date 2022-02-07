from rest_framework.serializers import ModelSerializer
from base.models import User, Room, Message

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'