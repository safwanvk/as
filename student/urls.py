from django.urls import path

from .views import *

urlpatterns = [
    path('login', student_login)
]
