from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'date', 'event_room', 'event_time')
    search_fields = ('event_name',)
    list_filter = ('date', 'event_time')


admin.site.register(Event, EventAdmin)
