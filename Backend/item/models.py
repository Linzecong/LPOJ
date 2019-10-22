# -*- coding: utf-8 -*-
from django.db import models
from user.models import User
import datetime

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(default="待补题",null=False)
    detail = models.TextField(null=True,blank=True)
    createtime = models.DateTimeField(null=False,default=datetime.datetime.now)
    deadtime = models.DateTimeField(null=True,default=datetime.datetime.now)
    status = models.IntegerField(default=1) # 1 新建 0 已完成
    tag = models.IntegerField(default=1) # 1 便签 # 2 待办事项 # 3 待补题

    objects = models.Manager()

    def __str__(self):
        
        return self.title

