from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MEMBER = "MEMBER", "Member"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    def __str__(self):
        return self.username