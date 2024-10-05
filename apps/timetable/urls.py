from django.urls import path
from .views import TeacherTimeTableView, StudentTimeTableView

urlpatterns = [
    path('timetable-student/', StudentTimeTableView.as_view(), name='timetable-student'),
    path('timetable-teacher/', TeacherTimeTableView.as_view(), name='timetable-teacher')
]
