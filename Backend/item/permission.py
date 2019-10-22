# coding=utf-8
from rest_framework import permissions
from .models import User


class UserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            return True
        if request.method == "GET":
            return False
        else:
            data = request.data
            username = str(data.get('user'))
            userid = request.session.get('user_id', None)
            if userid == username:
                return True
            else:
                return False

    def has_object_permission(self, request, view, item):
        if request.method == "GET":
            return False
        else:
            username = str(item.user.username)
            userid = request.session.get('user_id', None)
            if userid == username:
                return True
            else:
                return False

