from rest_framework import serializers
from .models import TeacherAvailability, TimeTableForLesson


class TimeTableForLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTableForLesson
        fields = '__all__'


class TeacherAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAvailability
        fields = '__all__'
