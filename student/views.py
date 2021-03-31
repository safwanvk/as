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
from django.contrib.auth.hashers import make_password
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

        print(serializer.data)

        if serializer.data.get('pass_hash') != make_password(password):
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

    # TODO: If expiry datetime precedes current datetime, return False

    return Response({"logged_in": True}, status=200)

