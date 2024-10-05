from rest_framework import serializers
from .models import Exam, ExamResult


class ExamSerializers(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class ExamResultSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = '__all__'
