from django.contrib import admin
from .models import Group, Grade, Classroom


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_teacher', 'grade')
    list_filter = ('main_teacher', 'grade')


admin.site.register(Group, GroupAdmin)
admin.site.register(Grade)
admin.site.register(Classroom)
