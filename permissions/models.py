import uuid

from django.db import models

from authentication.models import User


class Permission(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_school = models.CharField(default='Pending', max_length=20)
    status_warden = models.CharField(default='Pending', max_length=20)
    request_name = models.CharField(max_length=50)
    request_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def withdraw_request(self):
        self.delete()

    def approve_request(self, role):
        if role == 'Warden':
            self.status_warden = 'Approved'
        elif role == 'School':
            self.status_school = 'Approved'
        self.save()

    def edit_request(self, role):
        if role == 'Warden':
            self.status_warden = 'Pending'
        elif role == 'School':
            self.status_school = 'Pending'
        self.save()

    def reject_request(self, role):
        if role == 'Warden':
            self.status_warden = 'Rejected'
        elif role == 'School':
            self.status_school = 'Rejected'
        self.save()

    def __str__(self):
        return f'{self.request_name}'
