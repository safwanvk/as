from django.db import models

# Create your models here.
class Student(models.Model):
    sid = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=16)
    pass_hash = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Student"

class StudentLoginSessions(models.Model):
    sid = models.ForeignKey(Student,to_field='sid',on_delete=models.CASCADE, null=False)
    session_id = models.CharField(max_length=32,null=False)
    expires = models.DateTimeField(null=False)


    def __str__(self):
        return self.sid

    class Meta:
        db_table = "StudentLoginSessions"