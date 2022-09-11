from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Дает возможность админу создавать новых пользователей."""

    message = 'Доступно только для администратора'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'admin'
                    or request.user.is_superuser == True)
        return False

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                and request.user.is_authenticated):
            return True
        return (request.user.role == 'admin'
                or request.user.is_superuser == True)


class IsAdminOrReadOnly(permissions.BasePermission):

    message = 'Редактировать могут только администраторы'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                return True
        return False


class IsSelfUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Собственный класс разрешений"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)


class AdminModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in ('admin', 'moderator')
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
