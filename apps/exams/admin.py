from django.contrib import admin
from .models import Exam, ExamResult


class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'classroom', 'exam_date', 'exam_time', 'group')
    list_filter = ('subject__subject_name', 'group__grade', 'group__name')
    search_fields = ('subject', 'group__name')


admin.site.register(Exam, ExamAdmin)


class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'score', 'is_passed')
    list_filter = ('exam', 'exam__group__name', 'is_passed')
    search_fields = ('student__first_name', 'student__last_name')


admin.site.register(ExamResult, ExamResultAdmin)
