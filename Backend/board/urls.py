# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('board', views.BoardView)
routers.register('dailyboard', views.DailyBoardView)
routers.register('teamboard', views.TeamBoardView)
routers.register('dailycontestboard', views.DailyContestBoardView)

urlpatterns = [
    url('', include(routers.urls)),
]
