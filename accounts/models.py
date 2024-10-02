from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta


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
        extra_fields.setdefault('role', RoleCodes.ADMIN)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(print('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(print('Superuser must have is_staff=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class RoleCodes:
    GUEST = 'guest'
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'
    STAFF = 'staff'
    DIRECTOR = 'director'

    CHOICES = [
        (GUEST, 'Guest'),
        (STUDENT, 'Student'),
        (TEACHER,  'Teacher'),
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (DIRECTOR, 'Director'),
    ]


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    profile_photo = models.ImageField(upload_to='user_images/', default='default_img/img.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(choices=RoleCodes.CHOICES, max_length=100, default=RoleCodes.GUEST)
    password = models.CharField(max_length=128)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return (f""
                f"{self.first_name if self.first_name else self.username} "
                f"{self.last_name if self.last_name else self.phone_number}"
                )

    def save(self, *args, **kwargs):
        if self.role in [RoleCodes.STAFF, RoleCodes.DIRECTOR]:
            self.is_staff = True
        else:
            self.is_staff = False
        if self.role == RoleCodes.ADMIN:
            self.is_staff = True
            self.is_superuser = True

        else:
            self.is_superuser = False
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class NumberVerification(models.Model):
    phone_number = models.CharField(max_length=20)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=1)

    def __str__(self):
        return f'{self.phone_number} - {self.verification_code}'
