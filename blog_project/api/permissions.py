from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Данный Пермишен предоставляет доступ к чтению любому пользователялю,
    а ко пользователям с флагом is_staff или is_superuser - ко всем CRUD
    операциям c объектом.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )
