from rest_framework.views import APIView
from .serializers import ExamSerializers
from .models import Exam, ExamResult
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.permissions import IsStaff, IsAdmin, IsDirector, IsStudent, IsTeacher
from apps.accounts.models import User, RoleCodes


class ExamsView(APIView):
    def get(self, request):
        exam = Exam.objects.filter(group__students=request.user)

        if request.user.role in [RoleCodes.ADMIN, RoleCodes.STAFF, RoleCodes.DIRECTOR, RoleCodes.TEACHER]:
            exams = Exam.objects.all()
            serializers = ExamSerializers(exams, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)

        elif exam.exists():
            serializer = ExamSerializers(exam, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "In your group, there are no exams"},
            status=status.HTTP_404_NOT_FOUND
        )

    def post(self, request):
        serializers = ExamSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Not authorized"}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsTeacher | IsAdmin | IsStudent | IsDirector]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdmin | IsStaff | IsDirector]
        return super().get_permissions()


class ExamResultView(APIView):
    def get(self, request, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)

            if request.user == exam.examiner or request.user.role == RoleCodes.ADMIN:
                students = exam.group.students.all()
                results = []

                for student in students:
                    result = ExamResult.objects.filter(exam=exam, student=student).first()
                    results.append({
                        "student": student.get_full_name(),
                        "score": result.score if result else None,
                        "is_passed": result.is_passed if result else None
                    })

                return Response(results, status=status.HTTP_200_OK)

            elif request.user.role == RoleCodes.STUDENT:
                result = ExamResult.objects.filter(exam=exam, student=request.user).first()

                if result:
                    return Response({
                        "student": request.user.get_full_name(),
                        "score": result.score,
                        "is_passed": result.is_passed
                    }, status=status.HTTP_200_OK)

                return Response({"detail": "You have no results for this exam"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        except Exam.DoesNotExist:
            return Response({"detail": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, exam_id):
        try:
            exam = Exam.objects.get(id=exam_id)

            if request.user == exam.examiner or request.user.role == RoleCodes.ADMIN:
                data = request.data.get('results', [])

                for result_data in data:
                    student_id = result_data.get('student_id')
                    score = result_data.get('score')

                    group_student = exam.group.students.filter(id=student_id).exists()
                    if group_student:
                        student = User.objects.get(id=student_id)
                        is_passed = score >= exam.exam_passing_score

                        ExamResult.objects.update_or_create(
                            exam=exam,
                            student=student,
                            defaults={
                                'score': score,
                                'is_passed': is_passed
                            }
                        )
                    else:
                        return Response({"detail": f"This exam is not for student with ID {student_id}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                return Response({"detail": "Exam results have been created"}, status=status.HTTP_201_CREATED)

            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        except Exam.DoesNotExist:
            return Response({"detail": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAdmin | IsTeacher | IsStaff | IsStudent]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdmin | IsTeacher | IsStaff]
        return super().get_permissions()

