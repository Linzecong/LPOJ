# -*- coding: utf-8 -*-

from django.db import models

class User(models.Model):

    username = models.CharField(max_length=50,null=False,primary_key=True)
    password = models.CharField(max_length=50,null=False)
    name = models.CharField(max_length=50,null=False) #名称
    regtime = models.DateTimeField(auto_now=True)
    logintime = models.DateTimeField(auto_now=True)
    school = models.CharField(max_length=50,null=False)
    course = models.CharField(max_length=50,null=False)
    classes =  models.CharField(max_length=50,null=False)
    number = models.CharField(max_length=50,null=False)
    realname = models.CharField(max_length=50,null=False)
    qq = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=50,null=True)
    type = models.IntegerField(null=False,default=1) # 1 普通 2 管理员 3 超级管理员

    objects = models.Manager()

    def __str__(self):
        return self.username



class UserData(models.Model):

    username = models.CharField(max_length=50,null=False,primary_key=True)
    ac = models.IntegerField(null=False,default=0)
    submit = models.IntegerField(null=False,default=0)
    score = models.IntegerField(default=0)
    des = models.CharField(max_length=500,null=True)
    rating = models.IntegerField(default=1500)
    
    objects = models.Manager()

    def __str__(self):
        return self.username
