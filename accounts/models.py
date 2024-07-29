from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class ROLE(models.TextChoices):
        DEVELOPER = "DEV", "Developer"
        MANAGER = "MAN", "Manager"

    role = models.CharField(
        max_length=200, choices=ROLE.choices, default=ROLE.DEVELOPER
    )

    def is_developer(self):
        return self.role == User.ROLE.DEVELOPER

    def is_manager(self):
        return self.role == User.ROLE.MANAGER
