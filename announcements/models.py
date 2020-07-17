import uuid

from django.db import models

from authentication.models import User


class Announcement(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)

    def __str__(self):
        return f'{self.message}'
