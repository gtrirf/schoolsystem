from rest_framework import generics
from .serializers import GroupSerializer, RemoveStudentsSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Group, User
from .serializers import AddStudentsSerializer
from apps.accounts.permissions import IsStaff, IsAdmin, IsTeacher, IsDirector


class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsDirector | IsTeacher | IsAdmin | IsStaff]
        return super().get_permissions()


class GroupDetailView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsDirector | IsTeacher | IsAdmin | IsStaff]
        return super().get_permissions()


class AddStudentsToGroupView(APIView):
    def post(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"detail": "Group is not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddStudentsSerializer(data=request.data)
        if serializer.is_valid():
            student_ids = serializer.validated_data['student_ids']
            students = User.objects.filter(id__in=student_ids)
            group.students.add(*students)
            group.save()
            return Response({"detail": "Students successfully joined the group"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsDirector | IsTeacher | IsAdmin | IsStaff]
        return super().get_permissions()


class RemoveStudentsFromGroupView(APIView):
    def post(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RemoveStudentsSerializer(data=request.data)
        if serializer.is_valid():
            student_ids = serializer.validated_data['student_ids']
            students = User.objects.filter(id__in=student_ids)
            group.students.remove(*students)
            group.save()
            return Response({"detail": "Students removed from the group"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsDirector | IsTeacher | IsAdmin | IsStaff]
        return super().get_permissions()

