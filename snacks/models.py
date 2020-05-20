import uuid

from django.db import models

from authentication.models import User


class Snack(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    notify_students = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.date}'


class Bill(models.Model):
    snack_uid = models.ForeignKey(Snack, on_delete=models.CASCADE)
    creation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=4)
    bill = models.ImageField(upload_to='bills', blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.creation_user.first_name} {self.creation_user.last_name} - {self.snack_uid.date}'
