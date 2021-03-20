from django.db import models

# Create your models here.
class Student(models.Model):
    sid = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "student"