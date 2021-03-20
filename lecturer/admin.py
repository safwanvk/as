from django.contrib import admin

from .models import Lecturer, LecturerLoginSession

# Register your models here.
admin.site.register(Lecturer)
admin.site.register(LecturerLoginSession)