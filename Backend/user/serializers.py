# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import User, UserData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserNoPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserNoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['type']


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'
