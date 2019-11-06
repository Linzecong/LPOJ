# coding=utf-8
from rest_framework import permissions
from contest.models import ContestInfo
import datetime
from board.models import SettingBoard

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
        userid = request.session.get('user_id', None)
        if userid == blog.user:
            return True
        
        
        setting = SettingBoard.objects.get(id=1)
        if setting.openstatus == False:
            return False

        if blog.contest == 0 or request.session.get('type', 1) != 1:
            return True

        info = ContestInfo.objects.get(id=blog.contest)
        if (datetime.datetime.now()-info.begintime).total_seconds()>info.lasttime:
            return True
        return False
