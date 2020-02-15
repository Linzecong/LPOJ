# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import theClasses,ClassStudentData
class ClassDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = theClasses
        fields = '__all__'

class ClassStudentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassStudentData
        fields = '__all__'


