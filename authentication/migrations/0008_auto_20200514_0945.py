# Generated by Django 3.0.6 on 2020-05-14 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20200514_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default_profile_picture.png', upload_to='profile_pictures'),
        ),
    ]
