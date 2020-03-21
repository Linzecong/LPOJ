# coding=utf-8
from rest_framework import permissions
from .models import ClassStudentData, theClasses

from board.models import SettingBoard
import datetime

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
        type = request.session.get('type', 1)
        if type == 2 or type == 3:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False
