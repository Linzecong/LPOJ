# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Wiki,MBCode,MBCodeDetail

class WikiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wiki
        fields = '__all__'

class WikiCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wiki
        exclude = ['value']

class MBCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MBCode
        fields = '__all__'

class MBCodeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MBCodeDetail
        fields = '__all__'

class MBCodeDetailNoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MBCodeDetail
        exclude = ['code']