# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('classes', views.ClassDataView)
routers.register('classStudent', views.ClassStudentDataView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^ADDclasses', views.ClassDataAPIView.as_view()),
    url(r'^AddClass', views.ClassStudentDataAPIView.as_view()),
    url(r'^DeleteClass', views.DeleteClassDataAPIView.as_view()),
    url(r'^QuitClass', views.QuitClassAPIView.as_view()),
]
