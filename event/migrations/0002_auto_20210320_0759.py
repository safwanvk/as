# Generated by Django 3.1.7 on 2021-03-20 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lecturer', '0001_initial'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='lecturer_username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturer.lecturer'),
        ),
    ]
