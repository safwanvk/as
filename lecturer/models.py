from django.db import models

# Create your models here.
class Lecturer(models.Model):
    username = models.CharField(null=False, primary_key=True, max_length=16)
    name = models.CharField(max_length=64)
    pass_hash = models.CharField(max_length=128)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "Lecturer"

class LecturerLoginSession(models.Model):
    lecturer_username = models.ForeignKey(Lecturer,to_field='username',on_delete=models.CASCADE, null=False)
    session_id = models.CharField(max_length=32,null=False)
    expires = models.DateTimeField(null=False)


    def __str__(self):
        return self.lecturer_username

    class Meta:
        db_table = "LecturerLoginSession"