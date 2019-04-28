# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('userdata', views.UserDataView)
routers.register('user', views.UserView)
routers.register('change', views.UserChangeView)
routers.register('changeall', views.UserChangeAllView)

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^register', views.UserRegisterAPIView.as_view()),
    url(r'^login', views.UserLoginAPIView.as_view()),
    url(r'^logout', views.UserLogoutAPIView.as_view()),
    url(r'^updaterating', views.UserUpdateRatingAPIView.as_view()),
]
