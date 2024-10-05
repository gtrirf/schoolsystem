from django.db import models
from apps.accounts.models import User


class Subject(models.Model):
    subject_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return self.subject_name


class Ratings(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    xp = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'ratings'

    def __str__(self):
        return f'{self.student} - {self.xp}'


class Timeslot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'timeslots'

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'


class DayOfWeek(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'days'

    def __str__(self):
        return self.name

