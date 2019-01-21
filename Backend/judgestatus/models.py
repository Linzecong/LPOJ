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
    code = models.TextField()
    testcase = models.IntegerField()
    message = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.user