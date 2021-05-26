from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class User(AbstractUser) :
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='images/',blank=True,null=True)

class UserManager(BaseUserManager):
    
    def create_superuser(self, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user