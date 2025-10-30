from rest_framework import permissions
class IsLibrarian(permissions.BasePermission):
    message="Only librarian can perform this action"
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and getattr(request.user,'Role',None))=='LIBRARIAN'

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user==request.user