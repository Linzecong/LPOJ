# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('problem', views.ProblemView)
routers.register('problemdata', views.ProblemDataView)
routers.register('problemtag', views.ProblemTagView)
routers.register('choiceproblem', views.ChoiceProblemView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^uploadfile', views.UploadFileAPIView.as_view()),
    url(r'^downloadfile/',views.filedown,name='download'),
    url(r'^showpic/',views.showpic,name='show_picture'),
]
