from rest_framework import serializers
from .models import Group, User


class GroupSerializer(serializers.ModelSerializer):
    main_teacher = serializers.StringRelatedField()
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'main_teacher', 'students', 'grade', 'created_at', 'updated_at']


class AddStudentsSerializer(serializers.Serializer):
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    def validate_student_ids(self, value):
        students = User.objects.filter(id__in=value)
        if len(students) != len(value):
            raise serializers.ValidationError("Some students were not found")
        return value


class RemoveStudentsSerializer(serializers.Serializer):
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
