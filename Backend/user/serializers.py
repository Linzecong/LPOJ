# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import User,UserData,UserSubmittion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'

class UserSubmittionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmittion
        fields = '__all__'