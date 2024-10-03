from django.db import models
from groups.models import Group, Classroom
from accounts.models import User
from additions.models import Subject, Timeslot


class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    examiner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    exam_date = models.DateField()
    exam_time = models.ForeignKey(Timeslot, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    exam_passing_score = models.PositiveIntegerField(default=50)

    class Meta:
        db_table = 'exam'

    def __str__(self):
        return f'exam {self.subject}'


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    is_passed = models.BooleanField(default=False)

    class Meta:
        db_table = 'exam_result'

    def __str__(self):
        return f'{self.student}'


