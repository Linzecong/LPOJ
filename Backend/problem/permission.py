# coding=utf-8
from rest_framework import permissions

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
        if request.method in permissions.SAFE_METHODS:
            return True

        type = request.session.get('type', 1)
        if type == 2 or type == 3:
            return True
        else:
            return False


class AuthOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getVisitorPermission(request) == False:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        type = request.session.get('type', 1)
        if type == 2 or type == 3:
            return True
        else:
            return False

    def has_object_permission(self, request, view, problem):
        if getVisitorPermission(request) == False:
            return False
        type = request.session.get('type', 1)
        if type == 2 or type == 3:
            return True
        return problem.auth == 1 or problem.auth == 3
