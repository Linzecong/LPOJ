# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import OJMessage, Blog


class OJMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OJMessage
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
