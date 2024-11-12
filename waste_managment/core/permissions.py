from rest_framework import permissions


class WorkerOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        pk = obj.pk
        return (
            request.user.organizations.filter(pk=pk).exists()
            or request.user.is_staff
        )
