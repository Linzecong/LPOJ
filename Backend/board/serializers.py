# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Board,OthersSubmit

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class OthersSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OthersSubmit
        fields = '__all__'
