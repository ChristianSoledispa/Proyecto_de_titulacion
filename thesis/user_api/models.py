from djongo import models
from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class AppUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, password)
		user.is_superuser = True
		user.save()
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
	# user_id = models.ObjectIdField(primary_key=True)
	# email = models.CharField(max_length=50, unique=True)
	# username = models.CharField(max_length=50)
	# USERNAME_FIELD = 'email'
	# REQUIRED_FIELDS = ['username']
	# objects = AppUserManager()
	# def __str__(self):
	# 	return self.username
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    is_active = models.BooleanField(('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = AppUserManager() # <-- THIS IS YOUR CUSTOM USER MANAGER CLASS

    USERNAME_FIELD = 'email' # <-- INCLUDE THIS LINE HERE!
    REQUIRED_FIELDS = []