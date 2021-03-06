from django.urls import path

from .views import *

urlpatterns = [
    path('login', student_login),
    path('session-check', session_check),
    path('create', create_student),
    path('delete/<pk>', delete_student),
    path('', get_student)
]
