from django.db import models
from organisation.models import *

from authentication.models import User

import uuid

# Create your models here.
class Form(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    enable = models.BooleanField("Enable", default=False)
    name = models.CharField("Form Name", max_length=255)
    roles = models.ManyToManyField(Role)
    department = models.ManyToManyField(Department)
    group = models.ManyToManyField(Group)
    
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    
    def __str__(self):
        return self.name
    
class Questions(models.Model):
    ANSWER_TYPES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('boolean', 'Boolean'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
        ('select', 'Select'),
        ('file', 'File'),
    )
    FILE_TYPE = (
        ('none', 'None'),
        ('image/*', 'Images (jpg, png, gif, etc.)'),
        ('application/pdf', 'PDF files'),
        ('application/msword', 'Word documents (.doc)'),
        ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'Word documents (.docx)'),
        ('text/csv', 'CSV files'),
        ('text/plain', 'Text files (.txt)'),
        ('application/vnd.ms-excel', 'Excel files (.xls)'),
        ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'Excel files (.xlsx)'),
        ('application/zip', 'ZIP archives'),
        ('*/*', 'All file types'),
    )
    
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    question = models.CharField("Question", max_length=2000, null=False, blank=False)
    required = models.BooleanField("Required", default=False)
    
    answer_type = models.CharField("Answer Type", max_length=30, choices=ANSWER_TYPES, default='text')
    min_len = models.IntegerField("Min Length (characters for text, MB for files)", default=0)
    max_len = models.IntegerField("Max Length (characters for text, MB for files)", default=10)
    options = models.TextField("Options seperated by ||", null=True, blank=True)
    file_type = models.CharField("File Type", max_length=150, default='none', choices=FILE_TYPE)
    
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    
    def __str__(self):
        return f"{self.question}"
    
class FormQuestion(models.Model):
    id = models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, unique=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    form_index = models.IntegerField("Form Index", default=0)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.form_index is None or self.form_index == 0:
            query = FormQuestion.objects.filter(form=self.form)
            if self.pk:
                query = query.exclude(pk=self.pk)
            
            last_index = query.aggregate(
                models.Max('form_index')
            )['form_index__max']
            
            self.form_index = (last_index or 0) + 1
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.form} - {self.question}"
    
class FormUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_name()} - {self.form.name}"
    
class FormResponse(models.Model):
    id = models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, unique=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    response = models.JSONField("User Response")
    
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    