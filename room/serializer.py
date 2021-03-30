from rest_framework import serializers

from .models import *

class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = '__all__'