from django.shortcuts import render

from django.db import IntegrityError
from rest_framework.parsers import JSONParser 

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializer import *
import datetime
import uuid
import validation

# Create your views here.

# Get lecturer's event history
# TODO: Methods like this need to be authenticated (lecturer can only get this info with valid login session)
@api_view(['GET'])
def lecturer_events(request, *args, **kwargs):
    try:
    
        lecturer_username = request.GET.get('username')

        if not lecturer_username:
            return Response({"message": "Invalid lecturer username"}, status=400)

        lec_ats = Event.objects.filter(lecturer_username=lecturer_username)

        if not lec_ats.exists():
            return Response({"message": "Lecturer Attendance Not Found"}, status=404)

        serializer = EventSerializer(lec_ats, many=True)
        return Response(serializer.data, status=200)
    
    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)

# Get event's details
@api_view(['GET'])
def  event_details(request, *args, **kwargs):
    try:
    
        event_id = request.GET.get('id')

        if not event_id:
            return Response({"message": "Invalid event ID"}, status=400)

        lec_ats = Event.objects.filter(event_id=event_id)

        if not lec_ats.exists():
            return Response({"message": "Event Not Found"}, status=404)

        lec_ats = lec_ats.first()
        serializer = EventSerializer(lec_ats)
        return Response(serializer.data, status=200)
    
    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)

# Start lesson by creating event
@api_view(['POST'])
def start_lesson(request, *args, **kwargs):

    data = JSONParser().parse(request)

    lecturer_username = data.get('username')
    room = data.get('room')
    start_str = data.get('start')
    end_str = data.get('end')

    # If any of the values are not consistent with what is stored, then a response
    # is returned saying "parameters are missing" and an error code 400 is returned.
    if not (lecturer_username and room and start_str and end_str):
        return Response({"message": "Parameters missing"}, status=400)

    try:
        start = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(e)
        return Response({"message": "Invalid datetime"}, status=400)

    try:
        event_id = str(uuid.uuid4()).replace('-', '')[:16]

        event = Event.objects.create(
                    event_id=event_id, 
                    room=room,
                    datetime_start=start,
                    datetime_end=end,
                    lecturer_username=Lecturer.objects.get(username=lecturer_username)
            )

        return Response({"event_id": event_id} ,status=200)

    except:
        return Response({"message": "Can't create new event"} ,status=200)


