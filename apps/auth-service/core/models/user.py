from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    line_user_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    profile_img_url = models.CharField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
