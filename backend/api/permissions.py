from rest_framework import permissions


class AccessOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.is_authenticated

        return (
            request.user.is_authenticated and request.user == obj.author
        )
