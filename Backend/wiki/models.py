from django.db import models


class Wiki(models.Model):

    username = models.CharField(max_length=50, default="std")  # 发布人的用户名
    type = models.CharField(max_length=50)  # 发布了哪篇文章
    value = models.TextField(default="暂无文本")
    time = models.DateTimeField(auto_now=True)
    group = models.CharField(max_length=50, null=True, default="")  # 新添加的算法的分类
    std = models.IntegerField(default=0)  # 是否是标准算法，0代表是，1代表新添加的算法
    title = models.CharField(max_length=50, null=True, default="")  # 新添加的算法标题

    objects = models.Manager()

    def __str__(self):
        return self.username


class MBCode(models.Model):

    username = models.CharField(
        max_length=50, default="std", primary_key=True)  # 发布人的用户名
    des = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.username


class MBCodeDetail(models.Model):

    username = models.CharField(max_length=50, default="std")  # 发布人的用户名
    title = models.CharField(max_length=50)
    des = models.CharField(max_length=1000, default="none")
    group = models.CharField(max_length=50, default="none")
    code = models.TextField(default="暂无代码")
    time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.username


class TrainningContest(models.Model):

    title = models.CharField(max_length=50)  # 标题
    des = models.CharField(max_length=500)
    tips = models.CharField(max_length=500, null=True,
                            blank=True, default="")  # 教程 | 隔开
    group = models.IntegerField()  # 第几章
    num = models.IntegerField()  # 第几关
    problem = models.CharField(
        max_length=500, null=True, blank=True, default="")  # 题目 | 隔开

    objects = models.Manager()

    def __str__(self):
        return self.title
