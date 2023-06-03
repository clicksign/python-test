from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_GROUPS = (
        (1, 'Admin'),
        (2, 'Client'),
        (3, 'Seller')
    )

    user_group = models.PositiveSmallIntegerField(choices=USER_GROUPS, default=2)

    def __str__(self):
        return self.username
