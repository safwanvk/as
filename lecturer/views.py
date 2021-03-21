from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
import validation
from .models import *
from .serializer import *
from datetime import datetime, timedelta
from django.db import IntegrityError
from rest_framework.parsers import JSONParser 
import hashlib
import uuid

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

        password_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()

        if serializer.data.get('pass_hash') != password_hash:
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