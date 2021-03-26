from rest_framework import serializers

from .models import *


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = '__all__'