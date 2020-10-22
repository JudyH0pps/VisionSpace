from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):    
    use_in_migrations = True    
    
    def create_user(self, id, email, nickname=None, password=None):        
        if not email :            
            raise ValueError('must have user email')        
        user = self.model(
            id = id,
            email = self.normalize_email(email),            
            nickname = nickname        
        )        
        user.set_password(password)        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, id, email, nickname=None, password=None):
        user = self.create_user(
            id = id,            
            email = self.normalize_email(email),            
            nickname = nickname,            
            password = password   
        )        
        user.is_admin = True        
        user.is_superuser = True        
        user.is_staff = True        
        user.save(using=self._db)        
        return user 

# Create your models here.
class Account(AbstractBaseUser):
    objects = UserManager()
    
    username = None

    id = models.CharField(
        max_length=20,
        null=False,
        unique=True,
        primary_key=True
    )

    nickname = models.CharField(
        max_length=20,
        null=True,
        unique=True
    )

    email = models.EmailField(        
        max_length=255,        
        unique=True,    
    )

    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)     
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'id'    
    REQUIRED_FIELDS = ['email', "nickname"]
