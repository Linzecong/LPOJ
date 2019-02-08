# -*- coding: utf-8 -*-

from django.db import models

class Problem(models.Model):

    problem = models.CharField(max_length=50)
    author = models.CharField(max_length=50, default="admin")
    addtime = models.DateTimeField(auto_now=True)
    oj = models.CharField(max_length=50, default="LPOJ")
    title = models.CharField(max_length=50)
    des = models.TextField()
    input = models.TextField()
    output = models.TextField()
    sinput = models.TextField()
    soutput = models.TextField()
    source = models.TextField()
    time = models.IntegerField()
    memory = models.IntegerField()
    hint = models.TextField(null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

class ProblemData(models.Model):
    problem = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
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

    objects = models.Manager()

    def __str__(self):
        return self.title

class ProblemTag(models.Model):
    tagname = models.CharField(max_length=50,unique=True)
    count = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.tagname
