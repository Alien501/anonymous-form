from django.contrib import admin

from django.contrib.admin import ModelAdmin

from .models import *

# Register your models here.
@admin.register(Form)
class FormAdmin(ModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]
    list_filter = ['roles',]