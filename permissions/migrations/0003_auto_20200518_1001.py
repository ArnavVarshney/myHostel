# Generated by Django 3.0.6 on 2020-05-18 02:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0009_auto_20200514_1228'),
        ('permissions', '0002_auto_20200514_1907'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Permissions',
            new_name='Permission',
        ),
    ]
