from django.db import models
from apps.accounts.models import User
from apps.timetable.models import TimeTableForLesson


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    timetable = models.ForeignKey(TimeTableForLesson, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons'

    def __str__(self):
        return self.title


class Assignment(models.Model):
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateTimeField()
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    xp_reward = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignment'

    def __str__(self):
        return f'{self.lesson}'


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'submissions'

    def __str__(self):
        return f'{self.student}'

