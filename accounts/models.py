from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff set to True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser set to True')
        return self.create_user(email=email, password=password, **extra_fields)
    

class User(AbstractUser):
    
    email = models.EmailField(unique=True, max_length=80, blank=False, null=False)
    username= models.CharField(max_length=45, blank=True, null=True)
    date_of_birth= models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", "date_of_birth"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

