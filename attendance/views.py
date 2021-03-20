from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
import validation
from .models import *
from .serializer import *

# Create your views here.


# Get student's attendance history
@api_view(['GET'])
def student_attendance(request, *args, **kwargs):
    std_id = request.GET.get('sid')
    try:
        std_id = validation.sid(std_id)
    except ValueError:
        return Response({"message": "No valid student ID (sid)"}, status=400)

    std_ats = Attendance.objects.filter(sid=std_id)
    if not std_ats.exists():
        return Response({}, status=404)
    obj = std_ats.first()
    serializer = StudentAttendanceSerializer(obj)
    return Response(serializer.data, status=200)