# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('putitem', views.ItemPutView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^item', views.ItemGetAPIView.as_view()),
]
