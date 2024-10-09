from rest_framework.views import APIView
from .models import Ratings
from .serializers import RatingSerializers
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.permissions import IsStaff, IsAdmin, IsDirector, IsStudent, IsTeacher
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample


class RatingView(APIView):
    def get(self, request):
        student_rating = Ratings.objects.filter(student=request.user).first()
        if student_rating:
            serializer = RatingSerializers(student_rating)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "Rating not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        request=RatingSerializers,
        responses={200: RatingSerializers},
    )
    def post(self, request):
        serializer = RatingSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": "Not authorized"},
            status=status.HTTP_403_FORBIDDEN
        )

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsTeacher | IsAdmin | IsStudent | IsDirector]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdmin | IsStaff]
        return super().get_permissions()


class RatingListView(APIView):
    def get(self, request):
        student = request.user

        ratings = Ratings.objects.select_related('student').order_by('-xp')

        ranking_list = []
        for rating in ratings:
            if rating.student:
                ranking_list.append({
                    "student_id": rating.student.id,
                    "student": f'{rating.student.first_name} {rating.student.last_name}',
                    "xp": rating.xp
                })
            else:
                print(f"Rating {rating} has no associated student.")
        if not ranking_list:
            return Response({"error": "No ratings available"}, status=status.HTTP_404_NOT_FOUND)

        students_rank = next(
            (index + 1 for index, rating in enumerate(ranking_list) if rating['student_id'] == student.id),
            None
        )

        if students_rank is None:
            return Response(
                {"error": "Student has no rating"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "student_rank": students_rank,
            "student_xp": next(rating['xp'] for rating in ranking_list if rating['student_id'] == student.id),
            "ranking_list": ranking_list
        }, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

