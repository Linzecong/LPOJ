# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Problem,ProblemData,ProblemTag

admin.site.register(Problem)
admin.site.register(ProblemData)
admin.site.register(ProblemTag)