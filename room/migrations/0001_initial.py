# Generated by Django 3.1.7 on 2021-03-27 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('building', models.CharField(max_length=64)),
                ('coordinates', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'Building',
            },
        ),
    ]