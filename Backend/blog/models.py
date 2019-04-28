from django.db import models


class OJMessage(models.Model):

    username = models.CharField(max_length=50)
    msg = models.CharField(max_length=500)
    time = models.DateField(auto_now=True)
    rating = models.IntegerField(default=1500)

    objects = models.Manager()

    def __str__(self):
        return self.username


class Blog(models.Model):

    username = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    summary = models.CharField(max_length=1000)
    time = models.CharField(max_length=50)

    objects = models.Manager()

    def __str__(self):
        return self.username
