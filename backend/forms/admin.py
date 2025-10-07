from django.conf import settings

if settings.USE_UNFOLD:
    from unfold.admin import ModelAdmin, TabularInline
else:
    from django.contrib.admin import ModelAdmin, TabularInline
     
from django.contrib import admin

from django.conf import settings

from django.utils.html import format_html

from .models import *

# Register your models here.

class FormQuestionInline(TabularInline):
    model = FormQuestion
    extra = 1
    fields = ['question', 'form_index']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['question']

class FormUserInline(TabularInline):
    model = FormUser
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    can_delete = False
    autocomplete_fields = ['user']

@admin.register(Form)
class FormAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ['name', 'form_link', 'submission_count']
    search_fields = ['name',]
    list_filter = ['roles',]
    inlines = [FormQuestionInline, FormUserInline]
    fieldsets = (
        ('Form Details', {'fields': ('id', 'name','enable')}),
        ('Form Configuration', {'fields': ('roles', 'department', 'group')}),
        ('Form Meta', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at', 'id']
    
    def form_link(self, obj):
        return format_html(f"<a target='_' href='{settings.CLIENT_URL}/form/edit/{obj.id}'>View Form</a>")
    
    def submission_count(self, obj):
        count = FormUser.objects.filter(form=obj).count()
        return count
    submission_count.short_description = 'Submissions'

@admin.register(Questions)
class QuestionsAdmin(ModelAdmin):
    list_display = ['id', 'question', 'answer_type']
    search_fields = ['question']
    list_filter = ['answer_type']
    
    fieldsets = (
        ('Question', {'fields': ('id', 'question',)}),
        ('Answer Config', {'fields': ('answer_type', 'min_len', 'max_len', 'required',)}),
        ('Answer', {'fields': ('options', 'file_type')}),
        ('Question Meta', {'fields': ('created_at', 'updated_at')})
    )
    
    readonly_fields = ['id', 'created_at', 'updated_at']
    
@admin.register(FormQuestion)
class FormQuestionAdmin(ModelAdmin):
    list_display = ['form', 'question', 'form_index']
    search_fields = ['form', 'question']
    autocomplete_fields = ['form', 'question']
    
    fieldsets = (
        ('Form Question', {'fields': ('id', 'form', 'question', 'form_index')}),
        ('Meta', {'fields': ('created_at', 'updated_at')})
    )
    
    readonly_fields = ['id', 'created_at', 'updated_at']
    
@admin.register(FormResponse)
class FormResponseAdmin(ModelAdmin):
    list_display = ['id', 'form', 'created_at', 'updated_at']
    search_fields = ['form']
    list_filter = ['form']
    
    fieldsets = (
        ('Response', {'fields': ('id', 'form')}),
        ('User Response', {'fields': ('response',)}),
        ('Meta', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def delete_queryset(self, request, queryset):
        for obj in queryset.all():
            obj.delete()
    
@admin.register(FormUser)
class FormUserAdmin(ModelAdmin):
    list_display = ['user', 'form', 'user__code', 'created_at']
    search_fields = ['user__code', 'user__email', 'form__name']
    list_filter = ['form', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['user', 'form']
    
    fieldsets = (
        ('Form Submission', {'fields': ('user', 'form')}),
        # ('User Info', {'fields': ('user__code',)}),
        ('Meta', {'fields': ('created_at', 'updated_at')}),
    )
    
    # def user_code(self, obj):
    #     return obj.user.code if obj.user.code else 'N/A'
    # user_code.short_description = 'User Code'
    