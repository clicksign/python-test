from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("buyer", "Buyer"),
        ("admin", "Admin"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="buyer", null=False)
    phone_number = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=100, null=False)
