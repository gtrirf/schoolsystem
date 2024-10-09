from rest_framework.permissions import BasePermission
from .models import Roles
from rest_framework.exceptions import PermissionDenied


class IsAdmin(BasePermission):
    """
    Custom permission to only allow admin users to access certain views.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied("You don't have any role.")
        return request.user.role.role == Roles.ADMIN


class IsGuest(BasePermission):
    """
    Custom permission to allow only guest users to access certain views.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied("You don't have any role.")
        return request.user.role.role == Roles.GUEST


class IsTeacher(BasePermission):
    """
    Custom permission to allow only teacher users to access certain views.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied("You don't have any role.")
        return request.user.role.role == Roles.TEACHER


class IsStudent(BasePermission):
    """
    Custom permission to allow only student users to access certain views.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied("You don't have any role.")
        return request.user.role.role == Roles.STUDENT


class IsStaff(BasePermission):
    """
    Custom permission to allow only staff users to access certain views.
    """
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied("You don't have any role.")
        return request.user.role.role == Roles.STAFF


class IsDirector(BasePermission):
    """
        Custom permission to allow only directors users to access certain views.
    """
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied("You don't have any role.")
        return request.user.role.role == Roles.DIRECTOR
