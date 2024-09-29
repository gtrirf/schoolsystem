from rest_framework import permissions
from .models import RoleCodes


class IsGuest(permissions.BasePermission):
    """
    Allows access only to users with the 'guest' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.GUEST


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.ADMIN


class IsStaff(permissions.BasePermission):
    """
    Allows access to 'staff' users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.STAFF


class IsStudent(permissions.BasePermission):
    """
    Allow access to 'user' users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.STUDENT


class IsTeacher(permissions.BasePermission):
    """
    Allow access to 'user' users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.TEACHER


class IsDirector(permissions.BasePermission):
    """
    Allow access to 'director' users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleCodes.DIRECTOR
