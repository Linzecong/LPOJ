# -*- coding: utf-8 -*-

from django.db import models


class Problem(models.Model):
    problem = models.CharField(max_length=50, primary_key=True)
    author = models.CharField(max_length=50, default="admin")
    addtime = models.DateTimeField(auto_now=True)
    oj = models.CharField(max_length=50, default="LPOJ")
    title = models.CharField(max_length=500)
    des = models.TextField()
    input = models.TextField()
    output = models.TextField()
    sinput = models.TextField()
    soutput = models.TextField()
    source = models.TextField() # 也可以用来存该OJ的Pro ID
    time = models.IntegerField()
    memory = models.IntegerField()
    hint = models.TextField(null=True)
    auth = models.IntegerField(default=1)  # 1公开 2私密 3 比赛中的题
    template = models.CharField(max_length=10000, default="请删除这行")

    objects = models.Manager()

    def __str__(self):
        return self.title

class ChoiceProblem(models.Model):
    ChoiceProblemId = models.IntegerField(default=-1)
    des = models.TextField()
    choiceA = models.TextField()
    choiceB = models.TextField()
    choiceC = models.TextField()
    choiceD = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.des


class ProblemData(models.Model):
    problem = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=500)
    level = models.IntegerField(default=5)
    submission = models.IntegerField(default=0)
    ac = models.IntegerField(default=0)
    mle = models.IntegerField(default=0)
    tle = models.IntegerField(default=0)
    rte = models.IntegerField(default=0)
    pe = models.IntegerField(default=0)
    ce = models.IntegerField(default=0)
    wa = models.IntegerField(default=0)
    se = models.IntegerField(default=0)
    tag = models.TextField(null=True)
    score = models.IntegerField(default=1000)
    auth = models.IntegerField(default=1)  # 1公开 2私密 3 比赛中的题
    oj = models.CharField(max_length=50, default="LPOJ")


    objects = models.Manager()

    def __str__(self):
        return self.title


class ProblemTag(models.Model):
    tagname = models.CharField(max_length=50, unique=True)
    count = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.tagname

