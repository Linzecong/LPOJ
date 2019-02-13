# -*- coding: utf-8 -*-

from django.db import models

class User(models.Model):

    username = models.CharField(max_length=50,null=False)
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
    type = models.IntegerField(null=False,default=1)
    

    objects = models.Manager()

    def __str__(self):
        return self.username