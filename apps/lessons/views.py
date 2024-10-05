from rest_framework import generics
from .models import Lesson, Assignment, Submission
from apps.timetable.models import TeacherAvailability
from .serializers import LessonSerializer, AssignmentSerializer, SubmissionSerializer
from rest_framework.exceptions import ValidationError
from apps.accounts.permissions import IsTeacher, IsAdmin, IsDirector, IsStudent
from collections import defaultdict
from apps.additions import Ratings


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        timetable = serializer.validated_data['timetable']

        teacher = timetable.teacher

        start_time = timetable.lesson_time.start_time
        end_time = timetable.lesson_time.end_time

        availability = TeacherAvailability.objects.filter(
            teacher=teacher,
            day_of_week=timetable.day_of_week,
            work_time__start_time__lte=start_time,
            work_time__end_time__gte=end_time
        ).exists()

        if not availability:
            raise ValidationError("You can't take a class at this time, "
                                  "another class conflicts or it's not your working time.")

        serializer.save()

    def get_permissions(self):
        self.permission_classes = [IsTeacher | IsAdmin | IsDirector]
        return super().get_permissions()


class AssignmentCreateView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def perform_create(self, serializer):
        teacher = self.request.user
        lesson = serializer.validated_data['lesson']

        if lesson.timetable.teacher != teacher:
            raise ValidationError("You can only create assignments for classes you have taken.")

        serializer.save(teacher=teacher)

    def get_permissions(self):
        self.permission_classes = [IsTeacher | IsAdmin | IsDirector]
        return super().get_permissions()


class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_student:
            groups = user.student_of_group.all()
            return Assignment.objects.filter(lesson__timetable__group__in=groups)

        elif user.is_teacher:
            return Assignment.objects.filter(teacher=user)

        else:
            raise ValidationError("Not authorized")

    def get_permissions(self):
        self.permission_classes = [IsStudent | IsTeacher]
        return super().get_permissions()


class AssignmentUpdateView(generics.UpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_object(self):
        assignment = super().get_object()
        if assignment.teacher != self.request.user:
            raise ValidationError("You can only update assignments that you have created yourself")
        return assignment

    def get_permissions(self):
        self.permission_classes = [IsTeacher]
        return super().get_permissions()


class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        student = self.request.user
        assignment = serializer.validated_data['assignment']

        if not assignment.lesson.timetable.group.students.filter(id=student.id).exists():
            raise ValidationError("You can only submit assignments in your group.")

        serializer.save(student=student)

    def get_permissions(self):
        self.permission_classes = [IsStudent | IsAdmin | IsTeacher]
        return super().get_permissions()


class SubmissionUpdateView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_update(self, serializer):
        submission = self.get_object()
        teacher = self.request.user

        if submission.assignment.teacher != teacher:
            raise ValidationError("You are not authorized to update this submission.")

        score = self.request.data.get('score')
        if score > 60:
            rating, created = Ratings.objects.get_or_create(
                student=submission.student,
            )
            rating.xp += submission.assignment.xp_reward
            rating.save()

        serializer.save()

    def get_permissions(self):
        self.permission_classes = [IsAdmin | IsTeacher | IsDirector]
        return super().get_permissions()


class TeacherSubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        teacher = self.request.user

        submissions = Submission.objects.filter(assignment__teacher=teacher)

        grouped_submission = defaultdict(list)

        for submission in submissions:
            group = submission.assignment.lesson.timetable.group
            grouped_submission[group].append(submission)

        return grouped_submission

        # return Submission.objects.filter(assignment__teacher=teacher)
    def get_permissions(self):
        self.permission_classes = [IsTeacher | IsAdmin | IsDirector]
        return super().get_permissions()
