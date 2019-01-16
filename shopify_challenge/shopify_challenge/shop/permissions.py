from rest_framework import permissions

class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to see and edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the shopping cart.
        return str(obj.user) == str(request.user)