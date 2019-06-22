# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import OJMessage, Blog,Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class OJMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OJMessage
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
