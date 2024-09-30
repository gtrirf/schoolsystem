from django.contrib import admin
from .models import Ratings, Subject, Timeslot, DayOfWeek


class RatingAdmin(admin.ModelAdmin):
    list_display = ('student', 'xp')
    search_fields = ('student__username', 'student__first_name', 'student__last_name')
    ordering = ('-xp',)


admin.site.register(Ratings, RatingAdmin)
admin.site.register(Subject)
admin.site.register(DayOfWeek)


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')


admin.site.register(Timeslot, TimeSlotAdmin)
