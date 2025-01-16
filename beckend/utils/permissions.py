from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Разрешает доступ только администраторам и тому кто создал объект
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        return obj.owner == user


class IsAdminOrStaff(BasePermission):
    """
    Разрешает доступ только администраторам и пользователям с ролью 'персонал'
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)
