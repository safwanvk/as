from django.urls import path
from .views import *

urlpatterns = [
    path('login/', lecturer_login)
]
