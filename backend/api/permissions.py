from rest_framework.permissions import BasePermission
from rest_framework import permissions


class AuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user or request.method in permissions.SAFE_METHODS:
            return True
    
        return False
    
class UserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if obj == request.user or request.method in permissions.SAFE_METHODS:
            return True
        return False