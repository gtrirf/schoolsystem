from django.contrib import admin
from .models import Attendance


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student__first_name', 'student__last_name', 'lesson', 'status')
    list_filter = ('status', 'lesson')
    search_fields = ('student__first_name', 'student__last_name')


admin.site.register(Attendance, AttendanceAdmin)

