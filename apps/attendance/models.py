from django.db import models
from apps.accounts.models import User
from apps.lessons.models import Lesson
from apps.additions.models import TimeCreatedAndUpdated


class Attendance(TimeCreatedAndUpdated):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'attendances'

    def __str__(self):
        return f'{self.student}'

