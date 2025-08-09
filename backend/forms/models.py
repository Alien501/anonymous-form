from django.db import models
from organisation.models import *

from time import timezone

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
    
class Questions(models.Model):
    ANSWER_TYPES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
        ('select', 'Select'),
        ('file', 'File'),
    )
    
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    question = models.CharField("Question", max_length=2000, null=False, blank=False)
    required = models.BooleanField("Required", default=False)
    answer_type = models.CharField("Answer Type", max_length=30, choices=ANSWER_TYPES, default='text')
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    
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