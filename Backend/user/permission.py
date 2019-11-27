# coding=utf-8
from rest_framework import permissions
from .models import User
from board.models import SettingBoard

def getVisitorPermission(request):
    setting = SettingBoard.objects.filter(id=1)
    if len(setting) != 0:
        if setting[0].openvisitor is False:
            userid = request.session.get('user_id', None)
            if userid:
                return True
            else:
                return False
        else:
            return True
    else:
        return True

class ManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getVisitorPermission(request) == False:
            return False
        if request.method in permissions.SAFE_METHODS or request.method=="POST":
            return True

        type = request.session.get('type', 1)
        if type == 2 or type == 3:
            return True
        else:
            return False

class UserSafePostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getVisitorPermission(request) == False:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.session.get('type', 1) == 3:
            return True

        if request.method == "POST":
            rating = request.data.get('rating', -1)
            acc = request.data.get('ac', -1)
            sub = request.data.get('submit', -1)
            sco = request.data.get('score', -1)
            type = request.data.get('type', -1)
            if type != -1:
                return False
            if rating != "" or acc != "" or sub != "" or sco != "":
                if rating == -1:
                    return True
                return False
            else:
                return True

        data = request.data
        username = data.get('username')
        rating = data.get('rating', -1)
        score = data.get('score', -1)
        ac = data.get('ac', -1)
        submit = data.get('submit', -1)

        if rating != -1 or score != -1 or ac != -1 or submit != -1:
            return False

        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) == 3:
            return True
        else:
            return False


class UserPUTOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getVisitorPermission(request) == False:
            return False
        if request.method != "PUT":
            return False

        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) == 3:
            return True
        else:
            return False

    def has_object_permission(self, request, view, blog):
        if getVisitorPermission(request) == False:
            return False
        if request.method != "PUT":
            return False
        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) == 3:
            return True
        else:
            return False


class AuthPUTOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getVisitorPermission(request) == False:
            return False
        if request.method != "PATCH" and request.method != "PUT":
            return False
        if request.session.get('type', 1) == 3:
            return True
        else:
            return False

    def has_object_permission(self, request, view, blog):
        if getVisitorPermission(request) == False:
            return False
        if request.method != "PATCH" and request.method != "PUT":
            return False
        if request.session.get('type', 1) == 3:
            return True
        else:
            return False
