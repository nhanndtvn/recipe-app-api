# Database models.
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    # Manager model for users.

    def create_user(self, email,password=None, **extra_field):
        # Create, save, and return a new user.

        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        # Create a supper user
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # User model in the system.

    # Define user model fields.
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #Define Manager
    objects = UserManager()

    """
    Define the field that using for authentication
    Replace USERNAME field by custom EMAIL field
    """
    USERNAME_FIELD= 'email'


# Recipe model
class Recipe(models.Model):
    # Define model fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Lấy từ file settings - AUTH_USER_MODEL
        on_delete = models. CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
