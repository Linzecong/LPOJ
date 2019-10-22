# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = '__all__'

