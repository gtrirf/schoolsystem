from rest_framework import permissions
from .models import RoleCodes


class IsGuest(permissions.BasePermission):
    """
    Allows access only to users with the 'guest' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.objects.get(code='GUEST').code


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.objects.get(code='ADMIN').code


class IsStaff(permissions.BasePermission):
    """
    Allows access to 'staff' users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.objects.get(code='STAFF').code


class IsStudent(permissions.BasePermission):
    """
    Allow access to 'student' users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.objects.get(code='STUDENT').code


class IsTeacher(permissions.BasePermission):
    """
    Allow access to 'teacher' users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.objects.get(code='TEACHER').code


class IsDirector(permissions.BasePermission):
    """
    Allow access to 'director' users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.objects.get(code='DIRECTOR').code
