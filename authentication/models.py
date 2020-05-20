import binascii
import hashlib
import os
import uuid

from django.core.mail import send_mail
from django.db import models


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwd_hash = binascii.hexlify(pwd_hash)
    return (salt + pwd_hash).decode('ascii')


class User(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=False)
    password = models.CharField(max_length=500, blank=False)
    my_giis_id = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=8, blank=True)
    profile_picture = models.ImageField(default='profile_pictures/default_profile_picture.png',
                                        upload_to='profile_pictures', blank=True)
    isEmailVerified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    role_choices = (
        (1, 'Student'),
        (2, 'Warden'),
        (3, 'School'),
    )
    role = models.PositiveSmallIntegerField(choices=role_choices, null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

    def verify_email(self):
        self.isEmailVerified = True
        self.save()

    def reset_password(self, new_password):
        self.password = hash_password(new_password)
        self.save()

    def send_verification_email(self, host, scheme):
        message = f"Hello,\n\nFollow this link to verify your email " \
                  f"address.\n\n{scheme}://{host}/authentication/verify_email/?uid={self.uid}\n\nIf " \
                  f"you didn’t ask to verify this address, you can ignore this email.\n\nThanks,\n\nYour myHostel team "
        send_mail(subject="Verify your email for myHostel", message=message, recipient_list=[self.email],
                  from_email="myhostelgiis@gmail.com")

    def send_forgot_password_email(self, host, scheme):
        message = f"Hello,\n\nFollow this link to reset your password " \
                  f"address.\n\n{scheme}://{host}/authentication/reset_password/?uid={self.uid}\n" \
                  f"\nIf you didn’t ask to reset your password, you can ignore this email.\n\nThanks,\n\nYour " \
                  f"myHostel team "
        send_mail(subject="Reset your password for myHostel", message=message, recipient_list=[self.email],
                  from_email="myhostelgiis@gmail.com")
