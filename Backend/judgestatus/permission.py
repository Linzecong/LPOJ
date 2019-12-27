# coding=utf-8
from rest_framework import permissions
from contest.models import ContestInfo
import datetime
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


class UserRatingOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getVisitorPermission(request) == False:
            return False
        data = request.data
        username = data.get('user')
        userid = request.session.get('user_id', None)
        r1 = data.get('rating')
        r2 = request.session.get('rating', None)
        if r1 != r2:
            return False
        if userid == username or request.session.get('type', 1) != 1:
            return True
        else:
            return False

    def has_object_permission(self, request, view, blog):
        if getVisitorPermission(request) == False:
            return False
        data = request.data
        username = data.get('user')
        userid = request.session.get('user_id', None)
        r1 = data.get('rating')
        r2 = request.session.get('rating', None)
        if r1 != r2:
            return False
        if userid == username or request.session.get('type', 1) != 1:
            return True
        else:
            return False


class NoContestOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, blog):
        if getVisitorPermission(request) == False:
            return False

        if request.session.get('type', 1) != 1:
            return True

        setting = SettingBoard.objects.get(id=1)
        userid = request.session.get('user_id', None)

        if userid == blog.user:
            if setting.openstatus == False:
                return False
            return True

        if setting.openstatus == False:
            return False

        if blog.contest == 0:
            return True

        info = ContestInfo.objects.get(id=blog.contest)
        if (datetime.datetime.now()-info.begintime).total_seconds()>info.lasttime:
            return True
        return False
