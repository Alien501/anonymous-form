from django.contrib import admin

from django.conf import settings

if settings.USE_UNFOLD:
    from unfold.admin import ModelAdmin
else:
    from django.contrib.admin import ModelAdmin

from .models import *

# Register your models here.
@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ['role_name']
    search_fields = ['role_name']
    
@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = ['department_name']
    search_fields = ['department_name']

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ['group_name']
    search_fields = ['group_name']
