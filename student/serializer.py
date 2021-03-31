from rest_framework import serializers

from .models import *


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

class StudentLoginSessionSerializer(serializers.ModelSerializer):

    class Meta:

        model = StudentLoginSessions
        fields = '__all__'