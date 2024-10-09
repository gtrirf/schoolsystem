from rest_framework import serializers
from .models import Attendance


class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    status = serializers.BooleanField(required=False)

    class Meta:
        model = Attendance
        fields = ['student', 'student_name', 'status']


class AttendanceDetailSerializer(serializers.Serializer):
    student = serializers.IntegerField()
    status = serializers.BooleanField()


class AttendancePostSerializer(serializers.Serializer):
    lesson = serializers.IntegerField()
    attendances = AttendanceDetailSerializer(many=True)