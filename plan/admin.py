from django.contrib import admin
from .models import  Task,Kategories,dates,weecklines
# Register your models here.

admin.site.register(Task)

admin.site.register(Kategories)

admin.site.register(dates)

admin.site.register(weecklines)