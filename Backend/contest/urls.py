# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('contestannouncement', views.ContestAnnouncementView)
routers.register('contestcomment', views.ContestCommentView)
routers.register('contestinfo', views.ContestInfoView)
routers.register('contestcominginfo', views.ContestComingInfoView)
routers.register('contestproblem', views.ContestProblemView)
routers.register('contestboard', views.ContestBoardView)
routers.register('contestregister', views.ContestRegisterView)
routers.register('contestratingchange', views.ContestRatingChangeView)
routers.register('contesttutorial', views.ContestTutorialView)
routers.register('contesttotalboard', views.ContestBoardTotalView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^currenttime', views.CurrentTimeView.as_view()),
    url(r'^contestfilterboard', views.ContestBoardFilterAPIView.as_view()),
]
