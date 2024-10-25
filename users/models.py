from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser , PermissionsMixin
import uuid
# Create your models here.


class UserManager(BaseUserManager):
    
    def create_user(self,email,password=None, **extra_fields):
        if not email :
            raise ValueError({'email': "email must be provided"})
        user_email = self.normalize_email(email)
        user = self.model(email=user_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None, **extra_fields):

        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_admin',True)

        if extra_fields.get('is_superuser') is not True :
            raise ValueError({'is_superuser':"User must be a superuser"})
        if extra_fields.get('is_staff') is not True :
            raise ValueError({'is_staff': "user must have is_staff set to True"})
        if extra_fields.get('is_admin') is not True:
            raise ValueError({'is_admin': "user must have have is_staff set to true"})
        
        user = self.create_user(email=email , password=password , **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


IMAGE = "https://hngtask2bucket.s3.amazonaws.com/screenshots/pngtree-beautiful-profile-line-vector-icon-png-image_2035279.jpg"
class User(AbstractBaseUser, PermissionsMixin):

    full_name = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profile_img  = models.CharField(max_length=200, default=IMAGE)
    auth_provider = models.CharField(max_length=50, default="email")
    id = models.UUIDField(default=uuid.uuid4, editable=False , unique=True , primary_key=True)


    def __str__(self):
        return str(self.full_name)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

