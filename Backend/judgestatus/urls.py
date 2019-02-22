# -*- coding: utf-8 -*-


from django.conf.urls import url,include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('judgestatus', views.JudgeStatusView)
routers.register('judgestatusput', views.JudgeStatusPutView)

urlpatterns = [
    url('', include(routers.urls))
]
