from unittest import mock
from django.utils import timezone
import pytest
from rest_framework.test import APIClient
from faker import Faker
from apps.accounts.models import User, RoleCodes, NumberVerification
from apps.accounts.tools import Roles
from datetime import timedelta
from django.contrib.auth.hashers import make_password

fake = Faker()


@pytest.fixture
def create_roles(db):
    roles = [
        Roles.GUEST,
        Roles.ADMIN,
        Roles.STAFF,
        Roles.STUDENT,
        Roles.TEACHER,
        Roles.DIRECTOR
    ]
    for role in roles:
        RoleCodes.objects.get_or_create(role=role)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def guest_user(db, create_roles):
    phone_number = fake.phone_number()[:15]
    return User.objects.create_user(
        phone_number=phone_number,
        password=fake.password(),
        role=RoleCodes.objects.get(role=Roles.GUEST)
    )


@pytest.fixture
def student_user(db, create_roles):
    phone_number = fake.phone_number()[:15]
    return User.objects.create_user(
        phone_number=phone_number,
        password=fake.password(),
        role=RoleCodes.objects.get(role=Roles.STUDENT)
    )


@pytest.fixture
def teacher_user(db, create_roles):
    phone_number = fake.phone_number()[:15]
    return User.objects.create_user(
        phone_number=phone_number,
        password=fake.password(),
        role=RoleCodes.objects.get(role=Roles.TEACHER)
    )


@pytest.fixture
def director_user(db, create_roles):
    phone_number = fake.phone_number()[:15]
    return User.objects.create_user(
        phone_number=phone_number,
        password=fake.password(),
        role=RoleCodes.objects.get(role=Roles.DIRECTOR)
    )


@pytest.fixture
def staff_user(db, create_roles):
    phone_number = fake.phone_number()[:15]
    return User.objects.create_user(
        phone_number=phone_number,
        password=fake.password(),
        role=RoleCodes.objects.get(role=Roles.STAFF)
    )


@pytest.fixture
def admin_user(db, create_roles):
    phone_number = fake.phone_number()[:15]
    return User.objects.create_user(
        phone_number=phone_number,
        password=fake.password(),
        role=RoleCodes.objects.get(role=Roles.ADMIN)
    )


@pytest.fixture
def verification_code_expired(db):
    phone_number = fake.phone_number()[:15]
    with mock.patch('django.utils.timezone.now', return_value=timezone.now() - timedelta(minutes=6)):
        return NumberVerification.objects.create(
            phone_number=phone_number,
            verification_code=fake.random_number(digits=6),
            created_at=timezone.now()
        )


@pytest.fixture
def verification_code_recent(db):
    phone_number = fake.phone_number()[:15]
    with mock.patch('django.utils.timezone.now', return_value=timezone.now() - timedelta(seconds=30)):
        return NumberVerification.objects.create(
            phone_number=phone_number,
            verification_code=fake.random_number(digits=6),
            created_at=timezone.now()
        )


@pytest.mark.django_db
@pytest.fixture
def create_verified_number():
    def _create_verified_number(phone_number):
        verification = NumberVerification.objects.create(
            phone_number=phone_number,
            verification_code='123456',
            is_verified=True,
            created_at=timezone.now()
        )
        return verification
    return _create_verified_number


@pytest.mark.django_db
@pytest.fixture
def register_user(create_verified_number):
    def _register_user(phone_number):
        create_verified_number(phone_number)
        user = User.objects.create_user(
            phone_number=phone_number,
            username='testuser',
            password='password123'
        )
        return user
    return _register_user
