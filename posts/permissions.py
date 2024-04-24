from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsLoggedIn(BasePermission):
    def has_permission(self, request, view):
        print('IsLoggedIn class', request.user)
        print('Request.user.is_authenticated', request.user.is_authenticated)
        return request.user and request.user.is_authenticated
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print('IsOwner class', request.user)
        print('Obj.author', obj.author)
        return obj.author == request.user


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

