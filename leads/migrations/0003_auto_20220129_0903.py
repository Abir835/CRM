# Generated by Django 3.1.7 on 2022-01-29 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_auto_20220128_1839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user',
            new_name='user_profile',
        ),
    ]
