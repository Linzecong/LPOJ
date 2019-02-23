# -*- coding: utf-8 -*-

from django.db import models

class ContestInfo(models.Model):

    creator = models.CharField(max_length=50, default="admin")
    oj = models.CharField(max_length=50, default="LPOJ")
    title = models.CharField(max_length=50, default="contest")
    level = models.IntegerField(default=1)
    des = models.CharField(max_length=500, default="contest des")
    note = models.CharField(max_length=500, default="contest note")
    begintime = models.DateTimeField()
    lasttime = models.IntegerField(default=18000)
    type = models.CharField(max_length=50, default="ACM")
    auth = models.IntegerField(default=2) # 1 public 0 private 2 protect(需注册)

    objects = models.Manager()

    def __str__(self):
        return self.creator


class ContestAnnouncement(models.Model):

    contestid = models.IntegerField()
    announcement = models.CharField(max_length=500)
    
    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestProblem(models.Model):

    contestid = models.IntegerField()
    problemid = models.CharField(max_length=50)
    problemtitle = models.CharField(max_length=500,default="uname")
    rank = models.IntegerField() # 顺序 
    
    objects = models.Manager()

    def __str__(self):
        return self.contestid

class ContestBoard(models.Model):

    contestid = models.IntegerField()
    username = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    problemrank = models.IntegerField()
    type = models.IntegerField() # 1 AC 0没AC，算罚时
    submittime = models.IntegerField() # 秒为单位
    submitid = models.IntegerField() # 用于rejudge

    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestComment(models.Model):

    contestid = models.IntegerField()
    user = models.CharField(max_length=50)
    title = models.CharField(max_length=50,default="提问")
    problem = models.IntegerField(default=0) # 对哪个题目提问
    message = models.CharField(max_length=50)
    huifu = models.IntegerField(default=0) # 0代表是提问，其他数字代表回复了哪个提问
    time = models.DateTimeField()

    objects = models.Manager()

    def __str__(self):
        return self.contestid

class ContestRegister(models.Model):

    contestid = models.IntegerField()
    user = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)
    
    objects = models.Manager()

    def __str__(self):
        return self.contestid
