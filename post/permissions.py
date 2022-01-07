from  rest_framework import permissions
from rest_framework.permissions import  AllowAny,  IsAuthenticated, IsAdminUser
from rest_framework.permissions import SAFE_METHODS


class IsUserOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.id == obj.user.id  or request.user.is_staff)