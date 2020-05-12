# Generated by Django 3.0.6 on 2020-05-12 07:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('firstName', models.CharField(blank=True, max_length=50)),
                ('lastName', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('myGIISID', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('profilePicture', models.ImageField(default='defaultProfilePicture.jpg', upload_to='')),
                ('isEmailVerified', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Student'), (2, 'Warden'), (3, 'School')], null=True)),
            ],
        ),
    ]