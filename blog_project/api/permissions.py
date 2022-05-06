from rest_framework import permissions


class IsAdminAndOwnerOrCreateReadOnlyRoom(permissions.BasePermission):
    """
    Данный Пермишен предназначен для различения прав между пользователями
    относительно объектов комнат. Следующие варианты предусмотрены:
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


class IsAdminAndOwnerOrCreateOnlyMsg(permissions.BasePermission):
    """
    Данный Пермишен предназначен для различения прав между пользователями
    относительно объектов сообщений. Следующие варианты предусмотрены:
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
                and (request.user.is_staff or obj.user == request.user))
