from django.db import models


class Board(models.Model):

    username = models.CharField(max_length=50, primary_key=True)
    classes = models.CharField(max_length=50, default="")
    number = models.CharField(max_length=50, default="")
    OJCount = models.IntegerField(default=4)
    OJ = models.CharField(
        max_length=50, default="Codeforces|HDU|Vjudge|LPOJ|Others")
    account = models.CharField(max_length=50, default="###|###|###|###|###")
    acnum = models.CharField(max_length=50, default="0|0|0|0|0")
    submitnum = models.CharField(max_length=50, default="0|0|0|0|0")
    blogaddress = models.CharField(max_length=500, default="")

    objects = models.Manager()

    def __str__(self):
        return self.username


class DailyBoard(models.Model):

    username = models.CharField(max_length=50)
    account = models.IntegerField(default=0)
    collecttime = models.DateField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.username


class TeamBoard(models.Model):

    teammember = models.CharField(max_length=100)
    score = models.IntegerField(default=1500)
    collecttime = models.DateField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.teammember


class DailyContestBoard(models.Model):

    contestdate = models.DateField(auto_now=True)
    teammember = models.CharField(max_length=100)
    problemcount = models.IntegerField(default=0)
    wronglist = models.CharField(max_length=1000)  # A|B|C|F
    wrongtime = models.CharField(max_length=1000)  # 0|0|1|0  没AC必为0
    aclist = models.CharField(max_length=1000)  # A|B|C|F
    actime = models.CharField(max_length=1000)  # 00:10:50|0|0|0  没AC必为0

    objects = models.Manager()

    def __str__(self):
        return self.teammember

class SettingBoard(models.Model):


    schoolname = models.CharField(default="University",max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.teammember
