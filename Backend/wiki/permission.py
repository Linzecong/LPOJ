#coding=utf-8
from rest_framework import permissions

class UserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) != 1 :
            return True
        else:
            return False

    def has_object_permission(self, request, view, blog):
        if request.method in permissions.SAFE_METHODS:
            return True
        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) != 1 :
            return True
        else:
            return False