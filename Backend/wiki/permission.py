# coding=utf-8
from rest_framework import permissions
from board.models import SettingBoard

def getWikiPermission():
    setting = SettingBoard.objects.filter(id=1)
    if len(setting) != 0:
        if setting[0].openwiki is False:
            return False
        else:
            return True
    else:
        return False

class WikiUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getWikiPermission() == False:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True

        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) != 1:
            return True
        else:
            return False

    def has_object_permission(self, request, view, wiki):
        if getWikiPermission() == False:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        username = wiki.username
        userid = request.session.get('user_id', None)
        print(username, userid)
        if userid == username or request.session.get('type', 1) != 1:
            return True
        else:
            return False


class UserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getWikiPermission() == False:
            return False

        if request.method in permissions.SAFE_METHODS or request.method == "DELETE":
            return True

        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) != 1:
            return True
        else:
            return False

    def has_object_permission(self, request, view, blog):
        if getWikiPermission() == False:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        username = blog.username
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) != 1:
            return True
        else:
            return False


class ManagerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if getWikiPermission() == False:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.session.get('type', 1) == 3:
            return True
        else:
            return False

    def has_object_permission(self, request, view, blog):
        if getWikiPermission() == False:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.session.get('type', 1) == 3:
            return True
        else:
            return False
