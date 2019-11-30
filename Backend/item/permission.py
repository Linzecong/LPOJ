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

class UserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getVisitorPermission(request) == False:
            return False
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
        if getVisitorPermission(request) == False:
            return False
        if request.method == "GET":
            return False
        else:
            username = str(item.user.username)
            userid = request.session.get('user_id', None)
            if userid == username:
                return True
            else:
                return False

