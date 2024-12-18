from unittest import mock
from django.utils import timezone
import pytest
from rest_framework.test import APIClient
from faker import Faker
from apps.accounts.models import User, RoleCodes, NumberVerification
from apps.accounts.tools import Roles
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from apps.timetable.models import TimeTableForLesson
from apps.groups.models import Group
from apps.additions.models import Subject, DayOfWeek, Timeslot
from apps.events.models import Event
from apps.groups.models import Classroom

fake = Faker()


@pytest.fixture
def classroom(self):
    return Classroom.objects.create(name="Room A")


@pytest.fixture
def timeslot_for_event(self):
    return Timeslot.objects.create(start_time="10:00", end_time="11:00")


@pytest.fixture
def event(self, classroom, timeslot):
    return Event.objects.create(
        event_name="Test Event",
        date="2024-10-20",
        event_room=classroom,
        event_time=timeslot
    )


@pytest.fixture
def group(db):
    return Group.objects.create(name="Test Group")  # Adjust fields as necessary


@pytest.fixture
def subject(db):
    return Subject.objects.create(subject_name="Mathematics")  # Adjust fields as necessary


@pytest.fixture
def day_of_week(db):
    return DayOfWeek.objects.create(name="Monday")  # Adjust fields as necessary


@pytest.fixture
def timeslot(db):
    return Timeslot.objects.create(start_time="09:00", end_time="10:00")  # Adjust fields as necessary


@pytest.fixture
def timetable(db, group, subject, day_of_week, timeslot):
    return TimeTableForLesson.objects.create(
        group=group,
        subject=subject,
        teacher=User.objects.create_user(phone_number="teacher@example.com", password="password", role=RoleCodes.objects.get(role=Roles.TEACHER)),
        day_of_week=day_of_week,
        lesson_time=timeslot
    )


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
    role = RoleCodes.objects.get(role=Roles.ADMIN)
    return User.objects.create_user(
        phone_number=phone_number,
        password=fake.password(),
        role=role
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
            username=fake.name(),
            password='password123'
        )
        return user
    return _register_user


@pytest.fixture
def authenticated_client(self, api_client, create_roles, register_user):
    phone_number = '123123'
    user = register_user(phone_number)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client, refresh


