from django.db import models

from student.models import Student
from event.models import Event

# Create your models here.
class Attendance(models.Model):
    sid = models.ForeignKey(Student,to_field='sid',on_delete=models.CASCADE, null=False)
    arrival = models.DateTimeField(null=False)
    event_id = models.ForeignKey(Event,to_field='event_id',on_delete=models.CASCADE, null=False)


    def __str__(self):
        return self.sid

    class Meta:
        unique_together = (("sid", "event_id"),)

        db_table = "Attendance"