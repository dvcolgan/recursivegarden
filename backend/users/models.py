import logging

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    pass


class User(AbstractUser):
    objects = UserManager()

    def __str__(self):
        return self.username
