from django.shortcuts import render

from django.db import IntegrityError
from rest_framework.parsers import JSONParser 

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializer import *

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