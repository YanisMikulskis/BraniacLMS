# Register your models here.
from django.contrib import admin

from . import models as mainapp_models
@admin.register(mainapp_models.News)
class NewsAdmin(admin.ModelAdmin):
    pass



