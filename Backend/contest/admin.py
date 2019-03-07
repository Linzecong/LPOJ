# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ContestRank, ContestAnnouncement, ContestBoard, ContestComment, ContestInfo, ContestProblem, ContestRegister

admin.site.register(ContestAnnouncement)
admin.site.register(ContestBoard)
admin.site.register(ContestComment)
admin.site.register(ContestInfo)
admin.site.register(ContestProblem)
admin.site.register(ContestRank)
