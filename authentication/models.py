from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django_session_jwt.middleware.session import SessionMiddleware, BaseSessionMiddleware
from django.contrib.sessions.models import Session
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')


        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user




class User(AbstractBaseUser, PermissionsMixin):
    choice = [
        ('admin','admin'),
        ('worker','worker')
    ]
    kind_ = [
        ('ml','male'),
        ('fm','female')
    ]
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True, db_index=True , error_messages={'unique':_("this email is already exist ")})
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    kind = models.CharField(max_length=6 , choices=choice, null=True, blank=True)
    image = models.ImageField(null=True,blank=True)
    BirthOfDate = models.DateField(null=True,blank=True)
    sex = models.CharField(max_length=7, choices=kind_, null=True, blank=True)

    USERNAME_FIELD = ('email')
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    

