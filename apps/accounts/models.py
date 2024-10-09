from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from apps.additions.models import TimeCreatedAndUpdated
from .tools import Roles, CHOICES


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number field is required')

        user = self.model(
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        admin_role = RoleCodes.objects.get(role=Roles.ADMIN)
        extra_fields.setdefault('role', admin_role)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(print('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(print('Superuser must have is_staff=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class RoleCodes(models.Model):
    role = models.CharField(max_length=255, choices=CHOICES, unique=True)

    class Meta:
        db_table = 'rolecodes'

    def __str__(self):
        return f'{self.role}'


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    profile_photo = models.ImageField(upload_to='user_images/', default='default_img/img.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.ForeignKey(RoleCodes, on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return (f""
                f"{self.first_name if self.first_name else self.username} "
                f"{self.last_name if self.last_name else self.phone_number}"
                )

    def save(self, *args, **kwargs):
        if not self.role:
            try:
                guest_role = RoleCodes.objects.get(role=Roles.GUEST)
                self.role = guest_role
            except RoleCodes.DoesNotExist:
                raise ValueError("Guest role does not exist.")
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class NumberVerification(TimeCreatedAndUpdated):
    phone_number = models.CharField(max_length=20)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=1)

    def __str__(self):
        return f'{self.phone_number} - {self.verification_code}'
