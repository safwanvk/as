from rest_framework import serializers

from .models import *


class StudentAttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ['sid', 'arrival', 'event_id']

        