from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticatedOrReadOnly
)

LIST_ROLE = ['admin', 'moderator']


class IsAdminPermission(BasePermission):
    message = 'Данное действие доступно только администратору!'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    message = 'Данное действие доступно только администратору!'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == 'admin'
                )

    def has_object_permission(self, request, view, obj):
        """Определяем условие object_permission(user=admin)."""
        return request.method in SAFE_METHODS or request.user.role == 'admin'


class IsAuthenticatedOrReadOnlydAndAuthor(IsAuthenticatedOrReadOnly):
    message = 'Данное дейтвие вам не зазрешено!'

    def has_object_permission(self, request, view, obj):
        """Определяем условие object_permission(автор=юзер or staff)."""
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.role in LIST_ROLE
                )
