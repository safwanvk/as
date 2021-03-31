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
def student_login(request, *args, **kwargs):

    data = JSONParser().parse(request)
    print(data)

    std_id = data.get('std_id')
    password = data.get('password')

    print(std_id, password)

    if not std_id or not password:
        return Response('ValueError: std_id or Password not found', 400)

    try:
        std_id = validation.sid(std_id)
    except ValueError:
        return Response({"message": "Invalid student ID"}, status=400)

    try:
        std = Student.objects.filter(std_id=std_id)

        if not std.exists():
            return Response({"message": f"No Student found with student id {std_id}."}, status=404)

        lec = std.first()
        serializer = StudentSerializer(lec)

        ck = check_password(password, serializer.data.get('pass_hash'))

        if ck != True:
            return Response({"message": "Password incorrect"}, status=401)

        session_key = uuid.uuid4().hex
        key_expires = datetime.now() + timedelta(days=1)
        key_expires_string = key_expires.strftime("%Y-%m-%d %H:%M:%S")

        reg = StudentLoginSessions.objects.create(
                    sid=Student.objects.get(sid=std_id), 
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

    std_ses = StudentLoginSessions.objects.filter(session_id=session_id)

    if not std_ses.exists():
        return Response({"logged_in": False}, status=200)

    std_ses = std_ses.first()
    serializer = StudentLoginSessionSerializer(std_ses)

    # If expiry datetime precedes current datetime, return False
    dates = datetime.now()
    key_expires = dates.strftime("%Y-%m-%d %H:%M:%S")


    if serializer.data.get('expires') == key_expires:
        return Response({"logged_in": False}, status=200)

    return Response({"logged_in": True}, status=200)

# creating lecture
@api_view(['POST'])
def create_student(request, *args, **kwargs):

    data = JSONParser().parse(request)
    
    std_id = data.get('sid')
    username = data.get('username')
    name = data.get('name')
    password = data.get('password')

    # If any of the values are not consistent with what is stored, then a response
    # is returned saying "parameters are missing" and an error code 400 is returned.
    if not (std_id and username and name and password):
        return Response({"message": "Parameters missing"}, status=400)

    try:
        std_id = validation.sid(std_id)
    except ValueError:
        return Response({"message": "Invalid student ID"}, status=400)

    try:
        username = validation.username(username)
    except ValueError:
        return Response({"message": "Invalid Username"}, status=400)

    try:
        name = validation.name(name)
    except ValueError:
        return Response({"message": "Invalid Name"}, status=400)


    try:
        std = Student.objects.filter(sid=std_id)

        if std.exists():
            return Response({"message": f"Student already exist with student id {std_id}."}, status=404)
            

        student = Student.objects.create(
            sid=std_id,
            username=username, 
            name=name,
            pass_hash=make_password(password)
        )

        return Response({"msg": "Success"} ,status=200)

    except Exception as e:
        print(e)
        return Response({"message": "Can't Create Studeny"} ,status=200)

# delete studnet
@api_view(['DELETE'])
def delete_student(request, pk):

    try:

        try: 
            student = Student.objects.get(sid=pk) 
        except student.DoesNotExist: 
            return Response({'message': 'The Student does not exist'}, status=status.HTTP_404_NOT_FOUND) 

        student.delete() 
        return Response({'message': 'Student was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)

@api_view(['GET'])
def get_student(request, *args, **kwargs):
    try:
        students = Student.objects.all()
        
        students_serializer = StudentSerializer(students, many=True)
        for i in students_serializer.data:
            del i['pass_hash']
        return Response(students_serializer.data)

    except Exception as e:
        print(e)
        return Response({"message": "A server error occurred"}, status=500)

