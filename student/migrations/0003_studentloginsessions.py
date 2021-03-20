# Generated by Django 3.1.7 on 2021-03-20 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20210320_0719'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentLoginSessions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=32)),
                ('expires', models.DateTimeField()),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'db_table': 'StudentLoginSessions',
            },
        ),
    ]
