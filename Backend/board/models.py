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