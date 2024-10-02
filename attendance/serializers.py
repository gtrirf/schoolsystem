from rest_framework import serializers
from .models import Attendance


class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    status = serializers.BooleanField(required=False)

    class Meta:
        model = Attendance
        fields = ['student', 'student_name', 'status']
