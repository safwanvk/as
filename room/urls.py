from django.urls import path

from .views import *

urlpatterns = [
    path('', get_room),
    path('create', create_room),
    path('update/<pk>', update_room)
]
