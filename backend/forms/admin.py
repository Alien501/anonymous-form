from django.contrib import admin

from django.contrib.admin import ModelAdmin

from .models import *

# Register your models here.

class FormQuestionInline(admin.TabularInline):
    model = FormQuestion
    extra = 1
    fields = ['question', 'form_index']
    readonly_fields = ['form_index', 'created_at', 'updated_at']

@admin.register(Form)
class FormAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ['name',]
    search_fields = ['name',]
    list_filter = ['roles',]
    inlines = [FormQuestionInline]
    fieldsets = (
        ('Form Details', {'fields': ('id', 'name','enable')}),
        ('Form Configuration', {'fields': ('roles', 'department', 'group')}),
        ('Form Meta', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at', 'id']
    
@admin.register(Questions)
class QuestionsAdmin(ModelAdmin):
    list_display = ['id', 'question', 'answer_type']
    search_fields = ['question']
    list_filter = ['answer_type']
    
    fieldsets = (
        ('Question', {'fields': ('id', 'question', 'required')}),
        ('Answer', {'fields': ('answer_type',)}),
        ('Question Meta', {'fields': ('created_at', 'updated_at')})
    )
    
    readonly_fields = ['id', 'created_at', 'updated_at']
    
@admin.register(FormQuestion)
class FormQuestionAdmin(ModelAdmin):
    list_display = ['form', 'question', 'form_index']
    search_fields = ['form', 'question']
    
    fieldsets = (
        ('Form Question', {'fields': ('id', 'form', 'question', 'form_index')}),
        ('Meta', {'fields': ('created_at', 'updated_at')})
    )
    
    readonly_fields = ['id', 'form_index', 'created_at', 'updated_at']