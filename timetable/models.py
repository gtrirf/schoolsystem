from django.db import models
from accounts.models import User
from additions.models import Timeslot, Subject, DayOfWeek
from groups.models import Group


class TimeTableForLesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    day_of_week = models.ForeignKey(DayOfWeek, on_delete=models.SET_NULL, null=True, blank=True)
    lesson_time = models.ForeignKey(Timeslot, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'timetable'

    def __str__(self):
        return f'{self.subject} : {self.day_of_week}'


class TeacherAvailability(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    day_of_week = models.ManyToManyField(DayOfWeek, related_name='work_days', blank=True)
    work_time = models.ForeignKey(Timeslot, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'teachertime'

    def __str__(self):
        return f'{self.teacher}'

