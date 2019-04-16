from django.db import models

# Create your models here.
class Wiki(models.Model):

    username = models.CharField(max_length=50,default="std") # 发布人的用户名
    type = models.CharField(max_length=50) # 发布了哪篇文章
    value = models.TextField(default="暂无文本")
    time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.username

class MBCode(models.Model):

    username = models.CharField(max_length=50,default="std",primary_key=True) # 发布人的用户名
    des = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.username

class MBCodeDetail(models.Model):

    username = models.CharField(max_length=50,default="std") # 发布人的用户名
    title = models.CharField(max_length=50)
    des = models.CharField(max_length=50,default="none")
    group = models.CharField(max_length=50,default="none")
    code = models.TextField(default="暂无代码")
    time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.username