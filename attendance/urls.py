from django.urls import path

from .views import *

urlpatterns = [
    path('student-history/', student_attendance),
    path('register/', attend)
]