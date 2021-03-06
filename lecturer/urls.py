from django.urls import path
from .views import *

urlpatterns = [
    path('login', lecturer_login),
    path('session-check', session_check),
    path('create', create_lecturer),
    path('delete/<pk>', delete_lecturer),
    path('', get_lecturer)
]
