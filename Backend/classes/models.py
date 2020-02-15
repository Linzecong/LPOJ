# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.
class ClassStudentData(models.Model):
    studentUserName = models.CharField(max_length=50, null=False,default="")
    studentNumber = models.CharField(max_length=50, null=False)
    className = models.CharField(max_length=50, null=False)
    studentRealName = models.CharField(max_length=50, null=False)

    objects = models.Manager()

    def __str__(self):
        return self.studentName

class Classes(models.Model):
    className = models.CharField(max_length=50, null=False, primary_key=True)
    classSize = models.CharField(max_length=50, null=False)
    studentCount = models.CharField(max_length=50, null=False,default="0")

    objects = models.Manager()

    def __str__(self):
            return self.className


