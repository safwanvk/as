# Generated by Django 3.1.7 on 2021-03-26 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_building'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='coordinates',
            field=models.CharField(max_length=150),
        ),
    ]
