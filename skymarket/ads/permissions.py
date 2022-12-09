from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    message = 'Updating or deleting an add can be done by authors or admins only'

    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated and request.user.is_admin:
            return True

        if hasattr(obj, "author"):
            return request.user and request.user.is_authenticated and obj.author == request.user
