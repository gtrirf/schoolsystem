from rest_framework import serializers
from .models import Exam, ExamResult
from apps.accounts.models import User


class ExamSerializers(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class ExamResultSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = '__all__'


class ResultSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    score = serializers.IntegerField()

    def validate_student_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Student with this ID does not exist.")
        return value


class ResultsListSerializer(serializers.Serializer):
    results = ResultSerializer(many=True)

    def create(self, validated_data):
        results_data = validated_data.get('results')
        created_results = []
        for result in results_data:
            student_id = result['student_id']
            score = result['score']
            created_results.append(result)
        return {'results': created_results}
