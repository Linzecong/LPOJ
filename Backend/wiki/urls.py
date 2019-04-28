# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('wiki', views.WikiView)
routers.register('wikicount', views.WikiCountView)
routers.register('mbcode', views.MBCodeView)
routers.register('mbcodedetail', views.MBCodeDetailView)
routers.register('mbcodedetailnocode', views.MBCodeDetailNoCodeView)
routers.register('trainning', views.TrainningContestView)

urlpatterns = [
    url('', include(routers.urls)),
]
