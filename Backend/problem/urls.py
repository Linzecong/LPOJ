# -*- coding: utf-8 -*-


from django.conf.urls import url,include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('problem', views.ProblemView)
routers.register('problemdata', views.ProblemDataView)
routers.register('problemtag', views.ProblemTagView)

urlpatterns = [
    url('', include(routers.urls))
]

