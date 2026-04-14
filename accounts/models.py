from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    DONOR = 'donor'
    RECEIVER = 'receiver'
    ROLE_CHOICES = [
        (DONOR, 'Donor'),
        (RECEIVER, 'Receiver'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_donor(self):
        return self.role == self.DONOR

    def is_receiver(self):
        return self.role == self.RECEIVER

# Create your models here.
