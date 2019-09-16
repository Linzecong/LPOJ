# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('judgestatus', views.JudgeStatusView)
routers.register('judgestatusput', views.JudgeStatusPutView)
routers.register('judgestatuscode', views.JudgeStatusCodeView)
routers.register('casestatus', views.CaseStatusView)
routers.register('acrank', views.ACRankView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^rejudge', views.RejudgeAPIView.as_view()),
]
