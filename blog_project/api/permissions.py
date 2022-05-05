from rest_framework import permissions


class AdminAndOwnerOrCreateReadOnly(permissions.BasePermission):
    """
    Данный Пермишен предоставляет следующие права доступа:
    Anonym      - ReadOnly;
    User        - Read and Create;
    User.host   - Create, Read, Update, Destroy;
    Admin       - Create, Read, Update, Destroy;
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_staff or obj.host == request.user))
