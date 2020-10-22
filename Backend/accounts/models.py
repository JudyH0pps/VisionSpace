from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class Account(AbstractUser):
    nickname = models.CharField(
        max_length=20,
        null=True,
        unique=True
    )

    email = models.EmailField(        
        max_length=255,        
        unique=True,    
    )

    REQUIRED_FIELDS = ['email', "nickname"]
