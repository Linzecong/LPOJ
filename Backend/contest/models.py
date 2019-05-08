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
    auth = models.IntegerField(default=2)  # 1 public 2 private 0 protect(需注册)

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
    problemtitle = models.CharField(max_length=500, default="uname")
    rank = models.IntegerField()  # 顺序

    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestBoard(models.Model):

    contestid = models.IntegerField()
    username = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    problemrank = models.IntegerField()
    type = models.IntegerField()  # 1 AC， 0没AC算罚时，-1没AC不算罚时
    submittime = models.BigIntegerField()  # 豪秒为单位
    submitid = models.IntegerField()  # 用于rejudge
    rating = models.IntegerField(default=1500)

    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestRank(models.Model):

    contestid = models.IntegerField()
    username = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    # 用 | 分割，如  0|-1|100|0|-5 代表 B题错了一次，C题在100毫秒AC，
    statue = models.CharField(max_length=5000)
    rating = models.IntegerField(default=1500)
    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestComment(models.Model):

    contestid = models.IntegerField()
    user = models.CharField(max_length=50)
    title = models.CharField(max_length=50, default="提问")
    problem = models.CharField(default='ALL', max_length=500)  # 对哪个题目提问
    message = models.CharField(max_length=500)
    huifu = models.CharField(default="No respones", max_length=500)
    time = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=1500)

    objects = models.Manager()

    def __str__(self):
        return self.contestid

class ContestTutorial(models.Model):

    contestid = models.IntegerField()
    value = models.TextField(default="暂无数据！")

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


class ContestRatingChange(models.Model):

    contestid = models.IntegerField()
    contestname = models.CharField(max_length=100)
    contesttime = models.CharField(max_length=100)
    user = models.CharField(max_length=50)
    lastrating = models.IntegerField(default=0)
    ratingchange = models.IntegerField(default=0)
    currentrating = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestComingInfo(models.Model):

    ojName = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    startTime = models.BigIntegerField()
    endTime = models.BigIntegerField()
    contestName = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.contestName
