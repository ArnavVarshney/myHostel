# Generated by Django 3.0.6 on 2020-05-18 02:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0010_auto_20200518_1010'),
        ('snacks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snack',
            name='creation_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.User'),
            preserve_default=False,
        ),
    ]
