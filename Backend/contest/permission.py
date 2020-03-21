# coding=utf-8
from rest_framework import permissions
from .models import ContestInfo
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
        type = request.session.get('type', 1)
        if type == 2 or type == 3:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method=="POST":
            clone = request.data.get('clonefrom',-1)
            if clone == -1 :
                return True
            info = ContestInfo.objects.get(id=clone)
            if (datetime.datetime.now()-info.begintime).total_seconds()>info.lasttime:
                return True
                  
        return False


class UserRatingOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getVisitorPermission(request) == False:
            return False
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
        if getVisitorPermission(request) == False:
            return False
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

class UserOnly(permissions.BasePermission):



    def has_object_permission(self, request, view, blog):
        if getVisitorPermission(request) == False:
            return False

        if request.session.get('type', 1) != 1:
            return True

        userid = request.session.get('user_id', None)

        if userid == blog.username:
            return True
       

    