# Generated by Django 3.1.7 on 2022-01-22 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='call',
        ),
    ]
