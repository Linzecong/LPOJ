#coding=utf-8
from rest_framework import permissions
from .models import User
class LoginOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.session.get('user_id') is not None
        
    # def has_object_permission(self, request, view, blog):
    #     # Read permissions are allowed to any request,
    #     # so we'll always allow GET, HEAD or OPTIONS requests.
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return blog.owner.id == request.session.get('user_id')

class UserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method=="POST":
            return True
        
        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) == 3 :
            return True
        else:
            return False 

            
class UserPUTOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "PUT":
            return False
        
        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) == 3 :
            return True
        else:
            return False 
    
    def has_object_permission(self, request, view, blog):
        if request.method != "PUT":
            return False
        data = request.data
        username = data.get('username')
        userid = request.session.get('user_id', None)
        if userid == username or request.session.get('type', 1) == 3 :
            return True
        else:
            return False 
            

class AuthPUTOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "PUT":
            return False
        if request.session.get('type', 1) == 3 :
            return True
        else:
            return False 
    
    def has_object_permission(self, request, view, blog):
        if request.method != "PUT":
            return False
        if request.session.get('type', 1) == 3 :
            return True
        else:
            return False 