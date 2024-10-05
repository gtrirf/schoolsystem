from apps.timetable.serializers import TimeTableForLessonSerializer
from .models import TimeTableForLesson
from rest_framework import generics
from apps.accounts.permissions import IsStudent, IsAdmin, IsTeacher, IsDirector


class StudentTimeTableView(generics.ListAPIView):
    serializer_class = TimeTableForLessonSerializer

    def get_queryset(self):
        user = self.request.user
        groups = user.student_of_group.all()

        return TimeTableForLesson.objects.filter(group__in=groups)

    def get_permissions(self):
        self.permission_classes = [IsStudent | IsAdmin]
        return super().get_permissions()


class TeacherTimeTableView(generics.ListAPIView):
    serializer_class = TimeTableForLessonSerializer

    def get_queryset(self):
        user = self.request.user

        return TimeTableForLesson.objects.filter(teacher=user)
                
    def get_permissions(self):
        self.permission_classes = [IsTeacher | IsAdmin | IsDirector]
        return super().get_permissions()
