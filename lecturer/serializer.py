from rest_framework import serializers

from .models import *


class LecturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecturer
        fields = '__all__'

class LecturerLoginSessionSerializer(serializers.ModelSerializer):

    class Meta:

        model = LecturerLoginSession
        fields = '__all__'