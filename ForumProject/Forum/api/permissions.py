from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Only owner or read-only permission
    """
    message = "You must be an owner to update/delete this item"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author
