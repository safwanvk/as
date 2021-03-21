from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
import validation
from .models import *
from .serializer import *
import datetime
from django.db import IntegrityError
from rest_framework.parsers import JSONParser 

# Create your views here.


# Get student's attendance history
@api_view(['GET'])
def student_attendance(request, *args, **kwargs):
    try:

        std_id = request.GET.get('sid')

        try:
            std_id = validation.sid(std_id)
        except ValueError:
            return Response({"message": "No valid student ID (sid)"}, status=400)

        std_ats = Attendance.objects.filter(sid=std_id)
        if not std_ats.exists():
            return Response({"message": "Student Attendance Not Found"}, status=404)
        obj = std_ats.first()
        serializer = StudentAttendanceSerializer(obj)
        return Response(serializer.data, status=200)
    
    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)

# Endpoint called when student signs into their class
@api_view(['POST'])
def attend(request, *args, **kwargs):

    data = JSONParser().parse(request)
    print(data)

    std_id = data.get('user')
    event_uid = data.get('event')

    print(std_id, event_uid)

    if not std_id or not event_uid:
        return Response('ValueError: SID or Event_id not found', 400)

    try:
        try:
            std_id = validation.sid(std_id)
        except ValueError:
            return Response({"message": "Invalid student ID"}, status=400)

        try:
            event_uid = validation.event_id(event_uid)
        except ValueError:
            return Response({"message": "Invalid event ID"}, status=400)

        arrival = datetime.datetime.now()
        arrival = arrival.strftime("%Y-%m-%d %H:%M:%S")

        reg = Attendance.objects.create(
                    sid=Student.objects.get(sid=std_id), 
                    arrival=arrival,
                    event_id=Event.objects.get(event_id=event_uid),
            )

        return Response({"message": "Successfully signed in"} ,status=200)

            
    except IntegrityError:
        return Response({"message": "Already signed in"}, status=200)
    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)

# Get event's attendance history
@api_view(['GET'])
def event_attendance(request, *args, **kwargs):
    try:
    
        event_id = request.GET.get('event')

        if not event_id:
            return Response({"message": "Invalid event ID"}, status=400)

        event_ats = Attendance.objects.filter(event_id=event_id)
        if not event_ats.exists():
            return Response({"message": "Event Attendance Not Found"}, status=404)
        obj = event_ats.first()
        serializer = StudentAttendanceSerializer(obj)
        return Response(serializer.data, status=200)
    
    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)