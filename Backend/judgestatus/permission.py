#coding=utf-8
from rest_framework import permissions
class LoginOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.session.get('user_id') is not None
        
    def has_object_permission(self, request, view, blog):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        type = request.session.get('type', 1)
        
        if type == 2 or type == 3 :
            return True
        else:
            return False

class UserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        
        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) != 1 :
            return True
        else:
            return False

    def has_object_permission(self, request, view, blog):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) != 1 :
            return True
        else:
            return False

class NoContestOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, blog):
        
        userid = request.session.get('user_id', None)
        if userid == blog.user:
            return True

        contestid = blog.contest
        if contestid == 0 or request.session.get('type', 1) != 1 :
            return True
        else:
            return False

class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.session.get('type', 1) == 3 :
            return True
        else:
            return False

    def has_object_permission(self, request, view, blog):
        if request.session.get('type', 1) == 3 :
            return True
        else:
            return False