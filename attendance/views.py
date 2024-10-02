from rest_framework import viewsets
from .models import Attendance
from lessons.models import Lesson
from groups.models import Group
from .serializers import StudentAttendanceSerializer
from rest_framework.response import Response
from accounts.models import User
from accounts.permissions import IsTeacher, IsAdmin, IsDirector

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Attendance, Lesson, User
from .serializers import StudentAttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = StudentAttendanceSerializer

    def list(self, request, *args, **kwargs):
        lesson_id = request.query_params.get('lesson')
        if not lesson_id:
            return Response({"detail": "Lesson ID is required."}, status=400)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found."}, status=404)

        group = lesson.timetable.group
        students = group.students.all()

        attendances = []
        for student in students:
            attendance, created = Attendance.objects.get_or_create(lesson=lesson, student=student)
            attendances.append(attendance)

        serializer = StudentAttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        lesson_id = data.get('lesson')
        attendances = data.get('attendances', [])

        if not lesson_id or not attendances:
            return Response({"detail": "Lesson ID and students list must be"}, status=400)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found."}, status=404)

        for attendance_data in attendances:
            student_id = attendance_data.get('student')
            status_attendance = attendance_data.get('status')

            try:
                student = User.objects.get(id=student_id)
            except User.DoesNotExist:
                return Response({"detail": f"Student with ID {student_id} not found."}, status=404)

            Attendance.objects.update_or_create(
                lesson=lesson,
                student=student,
                defaults={'status': status_attendance}
            )

        return Response({"detail": "Attendance records updated successfully."}, status=200)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsTeacher | IsAdmin | IsDirector]
        else:
            self.permission_classes = [IsTeacher | IsAdmin | IsDirector]
        return super().get_permissions()

