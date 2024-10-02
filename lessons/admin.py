from django.contrib import admin
from .models import Lesson, Assignment, Submission


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'timetable', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'timetable__subject__name', 'timetable__teacher__username')
    list_filter = ('date', 'timetable__day_of_week', 'timetable__teacher')
    ordering = ('-date',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('description', 'teacher', 'due_date', 'lesson', 'xp_reward', 'created_at', 'updated_at')
    search_fields = ('description', 'teacher__username', 'lesson__title')
    list_filter = ('due_date', 'teacher', 'lesson__title')
    ordering = ('-due_date',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'score', 'updated_at')
    search_fields = ('assignment__description', 'student__username', 'score')
    list_filter = ('submitted_at', 'student', 'assignment__lesson__title', 'score')
    ordering = ('-submitted_at',)
