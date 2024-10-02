from django.db import models
from groups.models import Classroom
from additions.models import Timeslot


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    date = models.DateField()
    event_room = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    event_time = models.ForeignKey(Timeslot, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'events'

    def __str__(self):
        return self.event_name
