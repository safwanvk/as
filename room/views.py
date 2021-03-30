from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from django.db import IntegrityError
from rest_framework.parsers import JSONParser 

from .models import *
from .serializer import *
import validation


# Create your views here.

# Get room
@api_view(['GET'])
def get_room(request, *args, **kwargs):
    try:
    
        code = request.GET.get('code')

        if not code:
            return Response({"message": "Invalid code"}, status=400)

        try:
            code = validation.room_code(code)
        except ValueError:
            return Response({"message": "No valid code"}, status=400)

        room_dict = Building.objects.filter(code=code)

        if not room_dict.exists():
            return Response({"message": "Room Not Found"}, status=404)

        room_dict = room_dict.first()

        serializer = RoomSerializer(room_dict)
        return Response(serializer.data, status=200)
    
    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)

# creating room
@api_view(['POST'])
def create_room(request, *args, **kwargs):

    room_data = JSONParser().parse(request)
    room_serializer = RoomSerializer(data=room_data)
    if room_serializer.is_valid():
        room_serializer.save()
        return Response(room_serializer.data, status=status.HTTP_201_CREATED) 
    return Response(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update room
@api_view(['PUT'])
def update_room(request, pk):
    
    room_data = JSONParser().parse(request)

    try: 
        room = Building.objects.get(pk=pk) 
    except Building.DoesNotExist: 
        return Response({'message': 'The room does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    room_serializer = RoomSerializer(room, data=room_data) 
    if room_serializer.is_valid(): 
        room_serializer.save() 
        return Response(room_serializer.data) 
    return Response(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





