from django.db import models

# Create your models here.
class Building(models.Model):
    code = models.CharField(max_length=2,null=False, primary_key=True)
    building = models.CharField(max_length=64)
    coordinates = models.CharField(max_length=150)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "Building"