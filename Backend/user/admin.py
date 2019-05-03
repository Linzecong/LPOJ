from __future__ import unicode_literals

from django.contrib import admin
from .models import User,UserData

admin.site.register(User)
admin.site.register(UserData)