# -*- coding: utf-8 -*-


from django.conf.urls import url,include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()

urlpatterns = [
    url('', include(routers.urls)),
    url(r'^register',views.UserRegisterAPIView.as_view()),
    url(r'^login',views.UserLoginAPIView.as_view()),
]
