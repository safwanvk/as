from django.db import models
from lecturer.models import Lecturer

# Create your models here.
class Event(models.Model):
    event_id = models.CharField(max_length=16,null=False, primary_key=True)
    room = models.CharField(max_length=8)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    lecturer_username = models.ForeignKey(Lecturer,to_field='username',on_delete=models.CASCADE)

    def __str__(self):
        return self.event_id

    class Meta:
        db_table = "Event"
