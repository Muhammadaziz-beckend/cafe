from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        return obj.owner == user
