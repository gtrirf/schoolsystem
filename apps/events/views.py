from rest_framework import generics
from .serializers import EventSerializers
from .models import Event
from apps.accounts.permissions import IsAdmin, IsTeacher, IsDirector, IsStaff, IsStudent, IsGuest


class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializers

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsStaff | IsStudent | IsAdmin | IsTeacher | IsDirector | IsGuest]
        elif self.request.method == "POST":
            self.permission_classes = [IsStaff | IsAdmin | IsDirector]
        return super().get_permissions()


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializers

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsStaff | IsStudent | IsAdmin | IsTeacher | IsDirector | IsGuest]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsStaff | IsAdmin | IsDirector]
        return super().get_permissions()