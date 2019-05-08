# coding=utf-8
from rest_framework import permissions


class ManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        type = request.session.get('type', 1)
        if type == 2 or type == 3:
            return True
        else:
            return False


class UserRatingOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method=="PUT":
            return True

        # rating = request.data.get('rating', -1)
        # r2 = request.session.get('rating', 1)
        # if rating != r2:
        #     return False
        # else:
        #     return True

        if request.session.get('type', 1) == 3:
            return True

        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) == 3:
            return True
        else:
            return False


class UserRatingOnly2(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS  or request.method=="PUT":
            return True

        # rating = request.data.get('rating', -1)
        # r2 = request.session.get('rating', 1)
        # if rating != r2:
        #     return False
        # else:
        #     return True

        if request.session.get('type', 1) == 3:
            return True

        data = request.data
        username = data.get('user')

        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) == 3:
            return True
        else:
            return False
