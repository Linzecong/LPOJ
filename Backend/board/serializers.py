# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Board,OthersSubmit,DailyBoard,TeamBoard

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class DailyBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoard
        fields = '__all__'

class OthersSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OthersSubmit
        fields = '__all__'

class TeamBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamBoard
        fields = '__all__'