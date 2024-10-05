from django.contrib import admin
from .models import TimeTableForLesson, TeacherAvailability


@admin.register(TimeTableForLesson)
class TimeTableForLessonAdmin(admin.ModelAdmin):
    list_display = ('group', 'subject', 'teacher', 'day_of_week', 'lesson_time', 'created_at', 'updated_at')
    search_fields = ('subject__name', 'teacher__username', 'teacher__first_name', 'teacher__last_name', 'group__name')
    list_filter = ('day_of_week', 'subject', 'teacher')
    ordering = ('day_of_week', 'lesson_time')


@admin.register(TeacherAvailability)
class TeacherAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'work_time')
    search_fields = ('teacher__username', 'teacher__first_name', 'teacher__last_name')
    list_filter = ('teacher', 'day_of_week')
    ordering = ('day_of_week', 'work_time')
