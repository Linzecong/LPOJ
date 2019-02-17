# -*- coding: utf-8 -*-


from django.conf.urls import url,include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('userdata', views.UserDataView)
routers.register('usersubmittion', views.UserSubmittionView)
routers.register('user', views.UserView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^register',views.UserRegisterAPIView.as_view()),
    url(r'^login',views.UserLoginAPIView.as_view()),
]
