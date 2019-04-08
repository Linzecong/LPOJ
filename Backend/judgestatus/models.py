# -*- coding: utf-8 -*-

from django.db import models

class JudgeStatus(models.Model):

    user = models.CharField(max_length=50)
    oj = models.CharField(max_length=50, default="LPOJ")
    problem = models.CharField(max_length=50)
    result = models.IntegerField()
    time = models.IntegerField()
    memory = models.IntegerField()
    length = models.IntegerField()
    language = models.CharField(max_length=50)
    submittime = models.DateTimeField(auto_now=True)
    judger = models.CharField(max_length=50)
    contest = models.IntegerField()
    contestproblem = models.IntegerField(default=-1) # 对应比赛里的哪一题
    code = models.TextField()
    testcase = models.CharField(max_length=50,default="0")
    message = models.TextField()
    problemtitle = models.CharField(max_length=100,default="")
    

    objects = models.Manager()

    def __str__(self):
        return self.user


class CaseStatus(models.Model):

    statusid = models.IntegerField()
    username = models.CharField(max_length=50)
    problem = models.CharField(max_length=50)
    result = models.CharField(max_length=50,default="System Error")
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    testcase = models.CharField(max_length=50,default="unknow")
    casedata = models.CharField(max_length=500) # 非比赛才能查看，Judger中控制
    outputdata = models.CharField(max_length=500,default="") # 非比赛才能查看，Judger中控制
    useroutput = models.CharField(max_length=500,default="") # 非比赛才能查看，Judger中控制
    
    objects = models.Manager()

    def __str__(self):
        return self.statusid