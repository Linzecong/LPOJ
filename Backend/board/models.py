from django.db import models


class Board(models.Model):

    username = models.CharField(max_length=50,primary_key=True)
    classes = models.CharField(max_length=50,default="")
    number = models.CharField(max_length=50,default="")

    OJCount = models.IntegerField(default=3)
    OJ = models.CharField(max_length=50, default="Codeforces|HDU|Vjudge|Others")
    account = models.CharField(max_length=50, default="###|###|###|###")
    acnum = models.CharField(max_length=50, default="0|0|0|0")
    submitnum = models.CharField(max_length=50, default="0|0|0|0")

    objects = models.Manager()

    def __str__(self):
        return self.username

class OthersSubmit(models.Model):

    username = models.CharField(max_length=50)
    count = models.IntegerField(default=3)
    msg = models.CharField(max_length=500)
    accepted = models.IntegerField(default=0) # 0未审核，1审核通过，-1审核不通过

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
    score = models.IntegerField(default=0)
    collecttime = models.DateField(auto_now=True)  

    objects = models.Manager()

    def __str__(self):
        return self.teammember




class DailyContestBoard(models.Model):

    contestdate = models.DateField(auto_now=True)
    teammember = models.CharField(max_length=100)
    problemcount = models.IntegerField(default=0)
    wronglist = models.CharField(max_length=1000) # A|B|C|F
    wrongtime = models.CharField(max_length=1000) # 0|0|1|0  没AC必为0
    aclist = models.CharField(max_length=1000) # A|B|C|F
    actime = models.CharField(max_length=1000) # 00:10:50|0|0|0  没AC必为0

    objects = models.Manager()

    def __str__(self):
        return self.teammember