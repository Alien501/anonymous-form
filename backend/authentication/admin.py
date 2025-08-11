from django.contrib import admin
from django.conf import settings

if settings.USE_UNFOLD:
    from unfold.admin import ModelAdmin
else:
    from django.contrib.admin import ModelAdmin

from import_export.admin import ImportExportActionModelAdmin
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet

from .resources import UserResource
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin, ModelAdmin):
    # compressed_fields = True
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'code')}),
        ('Organisation Details', {'fields': ('role', 'department', 'group')}),
        ('Verification Status', {'fields': ('is_verified',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Other Info', {'fields': ('last_login', 'date_joined')}),
    )

    list_filter = ['is_active', 'is_staff', 'is_superuser',]
    search_fields = ['email', 'first_name', 'last_name',]
    list_display = ['email', 'first_name', 'last_name', 'code',]
    resource_classes = [UserResource]
    autocomplete_fields = ['role', 'department', 'group']
    
    def _create_log_entry(self, request, obj, change_message, change=False):
        user_id = request if isinstance(request, int) else request.user.pk
        
        if isinstance(obj, (list, tuple, QuerySet)):
            return [
                LogEntry.objects.log_action(
                    user_id=user_id,
                    content_type_id=ContentType.objects.get_for_model(item).pk,
                    object_id=item.pk,
                    object_repr=str(item),
                    action_flag=CHANGE if change else ADDITION,
                    change_message=change_message,
                )
                for item in obj
            ]
        else:
            return LogEntry.objects.log_action(
                user_id=user_id,
                content_type_id=ContentType.objects.get_for_model(obj).pk,
                object_id=obj.pk,
                object_repr=str(obj),
                action_flag=CHANGE if change else ADDITION,
                change_message=change_message,
            )