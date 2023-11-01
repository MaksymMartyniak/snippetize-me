from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def create_new_user(self):
        """Method for creating new user after first login"""
        pass
