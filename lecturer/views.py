from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
import validation
from .models import *
from .serializer import *
from datetime import datetime, timedelta
from django.db import IntegrityError
from rest_framework.parsers import JSONParser 
import uuid
from django.contrib.auth.hashers import *
from rest_framework import status

# Lecturer login
@api_view(['POST'])
def lecturer_login(request, *args, **kwargs):

    data = JSONParser().parse(request)
    print(data)

    username = data.get('username')
    password = data.get('password')

    print(username, password)

    if not username or not password:
        return Response('ValueError: Username or Password not found', 400)

    try:
        lec = Lecturer.objects.filter(username=username)

        if not lec.exists():
            return Response({"message": f"No lecturer found with username {username}."}, status=404)

        lec = lec.first()
        serializer = LecturerSerializer(lec)

        print(serializer.data)

        print(serializer.data.get('pass_hash'), make_password(password))

        ck = check_password(password, serializer.data.get('pass_hash'))

        if ck != True:
            return Response({"message": "Password incorrect"}, status=401)

        session_key = uuid.uuid4().hex
        key_expires = datetime.now() + timedelta(days=1)
        key_expires_string = key_expires.strftime("%Y-%m-%d %H:%M:%S")

        reg = LecturerLoginSession.objects.create(
                    lecturer_username=Lecturer.objects.get(username=username), 
                    session_id=session_key,
                    expires=key_expires_string)

        return Response({"session_key": session_key} ,status=200)

    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)

# Check login session is valid
@api_view(['GET'])
def session_check(request, *args, **kwargs):

    session_id = request.GET.get('session')

    if not validation.session_id_is_valid(session_id):
        return Response({"logged_in": False}, status=200)

    lec_ses = LecturerLoginSession.objects.filter(session_id=session_id)

    if not lec_ses.exists():
        return Response({"logged_in": False}, status=200)

    # TODO: If expiry datetime precedes current datetime, return False

    return Response({"logged_in": True}, status=200)


# creating lecture
@api_view(['POST'])
def create_lecturer(request, *args, **kwargs):

    data = JSONParser().parse(request)

    username = data.get('username')
    name = data.get('name')
    password = data.get('password')

    # If any of the values are not consistent with what is stored, then a response
    # is returned saying "parameters are missing" and an error code 400 is returned.
    if not (username and name and password):
        return Response({"message": "Parameters missing"}, status=400)

    try:
        username = validation.username(username)
    except ValueError:
        return Response({"message": "Invalid Username"}, status=400)

    try:
        name = validation.name(name)
    except ValueError:
        return Response({"message": "Invalid Name"}, status=400)


    try:
        lec = Lecturer.objects.filter(username=username)

        if lec.exists():
            return Response({"message": f"lecturer already exist with username {username}."}, status=404)
            

        lecturer = Lecturer.objects.create(
                    username=username, 
                    name=name,
                    pass_hash=make_password(password)
            )

        return Response({"msg": "Success"} ,status=200)

    except Exception as e:
        print(e)
        return Response({"message": "Can't create lecturer"} ,status=200)

# delete lecturer
@api_view(['DELETE'])
def delete_lecturer(request, pk):

    try:

        try: 
            lecturer = Lecturer.objects.get(username=pk) 
        except Lecturer.DoesNotExist: 
            return Response({'message': 'The Lecturer does not exist'}, status=status.HTTP_404_NOT_FOUND) 

        lecturer.delete() 
        return Response({'message': 'Lecturer was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)

@api_view(['GET'])
def get_lecturer(request, *args, **kwargs):
    try:
        lecturers = Lecturer.objects.all()
        
        lecturers_serializer = LecturerSerializer(lecturers, many=True)
        for i in lecturers_serializer.data:
            del i['pass_hash']
        return Response(lecturers_serializer.data)

    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)





