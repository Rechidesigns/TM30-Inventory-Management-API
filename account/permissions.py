from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsUserAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):

        if request.user and request.user.is_authenticated == True:
            return True
        else:
            raise PermissionDenied(detail= {"message": "Permission denied"})

class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff == True:

            return True

        else:

            raise PermissionDenied(detail={'message': 'Permission denied. User is not an admin'})

class IsUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'GET' and request.user.is_authenticated:

            return True
        else:
            if request.user.is_authenticated and request.user.is_staff == True:

                return True
            else:

                raise PermissionDenied(detail={'message': 'Permission denied. User is not an admin'})