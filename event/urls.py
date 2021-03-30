from django.urls import path
from .views import *

urlpatterns = [
    path('lecturer-history', lecturer_events),
    path('details/', event_details),
    path('start/', start_lesson)
]

