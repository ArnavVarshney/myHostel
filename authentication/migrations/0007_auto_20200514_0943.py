# Generated by Django 3.0.6 on 2020-05-14 01:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0006_auto_20200514_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_profile_picture.png', upload_to='profile_pictures'),
        ),
    ]
