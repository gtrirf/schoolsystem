from django.db import models
from apps.accounts.models import User
from apps.additions.models import TimeCreatedAndUpdated


class Grade(models.Model):
    grade = models.IntegerField()

    class Meta:
        db_table = 'grades'

    def __str__(self):
        return f'{self.grade}-grade'


class Group(TimeCreatedAndUpdated):
    name = models.CharField(max_length=100)
    main_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField(User, related_name='student_of_group', blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'groups'

    def __str__(self):
        return f'{self.grade}-{self.name}'


class Classroom(models.Model):
    room_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'classrooms'

    def __str__(self):
        return self.room_name

