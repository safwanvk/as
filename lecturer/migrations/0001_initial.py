# Generated by Django 3.1.7 on 2021-03-20 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('username', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('pass_hash', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'Lecturer',
            },
        ),
    ]
