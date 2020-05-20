import uuid

from django.db import models

from authentication.models import User


class WeeklyReport(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.date}'


class Report(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    weekly_report_uid = models.ForeignKey(WeeklyReport, on_delete=models.CASCADE)
    creation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.creation_user.first_name} {self.creation_user.last_name} - {self.weekly_report_uid.date}'
