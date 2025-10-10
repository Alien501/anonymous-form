from django.conf import settings

if settings.USE_UNFOLD:
    from unfold.admin import ModelAdmin, TabularInline
else:
    from django.contrib.admin import ModelAdmin, TabularInline
     
from django.contrib import admin

from django.conf import settings

from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.

class FormQuestionInline(TabularInline):
    model = FormQuestion
    extra = 1
    fields = ['question', 'form_index']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['question']
    tab = True  # Create tab for questions

class FormUserInline(TabularInline):
    model = FormUser
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    can_delete = False
    autocomplete_fields = ['user']
    tab = True  # Create tab for users

class FormResponseInline(TabularInline):
    """Custom inline to display form responses as a tab"""
    model = FormResponse
    extra = 0
    can_delete = False
    tab = True  # Create tab for responses
    verbose_name = "Response"
    verbose_name_plural = "Form Responses"
    template = "custom/forms/form_response_inline_tab.html"
    
    # Make it completely read-only
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        # Return empty queryset to prevent any form rendering
        return self.model.objects.none()
    
    def get_formset(self, request, obj=None, **kwargs):
        # Set validate_max to False to prevent validation errors
        kwargs['validate_max'] = False
        kwargs['validate_min'] = False
        
        formset_class = super().get_formset(request, obj, **kwargs)
        
        # Make the formset always valid and never save
        def always_valid(self):
            return True
        
        original_save = formset_class.save
        def no_save(self, commit=True):
            # Return empty lists for new_objects, changed_objects, deleted_objects
            self.new_objects = []
            self.changed_objects = []
            self.deleted_objects = []
            return []
        
        formset_class.is_valid = always_valid
        formset_class.save = no_save
        
        # Initialize defaults
        formset_class.response_table_data = {'headers': [], 'rows': []}
        formset_class.has_responses = False
        
        # Prepare response table data for the template (only for existing forms)
        if obj and obj.pk:
            # Get questions for this form
            form_questions = obj.formquestion_set.select_related('question').order_by('form_index')
            questions = [fq.question for fq in form_questions]
            
            # Get responses
            responses = obj.form_user_response.all().order_by('-created_at')
            
            # Prepare table data
            from django.urls import reverse
            
            # Build headers
            headers = ['#', 'Submitted At']
            headers.extend([q.question[:50] for q in questions])
            headers.append('Actions')
            
            # Build rows
            rows = []
            for idx, response in enumerate(responses, 1):
                row = [str(idx), response.created_at.strftime("%b %d, %Y %H:%M")]
                
                # Add answer cells
                for question in questions:
                    question_id = str(question.id)
                    answer_data = response.response.get(question_id, {})
                    
                    if answer_data:
                        answer_type = answer_data.get('answer_type')
                        value = answer_data.get('value')
                        
                        if answer_type == 'file' and value:
                            file_path = value.get('file_path', '')
                            file_name = value.get('file_name', 'View File')
                            if file_path:
                                cell = mark_safe(format_html(
                                    '<a href="/media/{}" target="_blank" class="text-primary-600 hover:text-primary-700 dark:text-primary-500 underline">📎 {}</a>',
                                    file_path, file_name[:30]
                                ))
                            else:
                                cell = mark_safe('<span class="text-base-400 italic">No file</span>')
                        elif answer_type == 'boolean':
                            if value:
                                cell = mark_safe('<span class="inline-flex items-center px-2.5 py-0.5 rounded-default text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">✓ Yes</span>')
                            else:
                                cell = mark_safe('<span class="inline-flex items-center px-2.5 py-0.5 rounded-default text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400">✗ No</span>')
                        elif answer_type == 'checkbox' and isinstance(value, list):
                            badges = ''.join([
                                format_html('<span class="inline-flex items-center px-2 py-1 rounded-default text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-900/30 dark:text-primary-400 mr-1">{}</span>', item)
                                for item in value
                            ])
                            cell = mark_safe(format_html('<div class="flex flex-wrap gap-1">{}</div>', mark_safe(badges))) if badges else '-'
                        else:
                            cell = str(value)[:150] if value else '-'
                    else:
                        cell = '-'
                    
                    row.append(cell)
                
                # Add actions column
                change_url = reverse('admin:forms_formresponse_change', args=[response.id])
                delete_url = reverse('admin:forms_formresponse_delete', args=[response.id])
                actions = mark_safe(format_html(
                    '<a href="{}" class="text-primary-600 hover:text-primary-700 dark:text-primary-500 font-medium">View</a> '
                    '<span class="mx-1 text-base-300">|</span> '
                    '<a href="{}" class="text-red-600 hover:text-red-700 dark:text-red-500 font-medium">Delete</a>',
                    change_url, delete_url
                ))
                row.append(actions)
                rows.append(row)
            
            # Attach to formset so template can access
            formset_class.response_table_data = {
                'headers': headers,
                'rows': rows
            }
            formset_class.has_responses = responses.exists()
        
        return formset_class
            
@admin.register(Form)
class FormAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ['name', 'form_link', 'submission_count']
    search_fields = ['name',]
    list_filter = ['roles',]
    inlines = [FormQuestionInline, FormUserInline, FormResponseInline]
    
    fieldsets = (
        ('Form Details', {'fields': ('id', 'name','enable')}),
        ('Form Configuration', {'fields': ('roles', 'department', 'group')}),
        ('Form Meta', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at', 'id']
    
    def get_inlines(self, request, obj=None):
        """Only show FormResponseInline when editing existing forms"""
        if obj and obj.pk:
            # Editing existing form - show all inlines including responses
            return [FormQuestionInline, FormUserInline, FormResponseInline]
        else:
            # Creating new form - don't show responses inline
            return [FormQuestionInline, FormUserInline]

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
    