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
    submission = models.IntegerField()
    accepted = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.title