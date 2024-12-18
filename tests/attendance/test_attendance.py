import pytest
from django.urls import reverse
from rest_framework import status
from apps.attendance.models import Attendance
from apps.lessons.models import Lesson
from apps.accounts.models import User
from apps.accounts.tools import Roles

