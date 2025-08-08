from django.db import models

import uuid

# Create your models here.
class Role(models.Model):
    role_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role_name = models.CharField("Role Name", max_length=250, blank=False)
    
    def __str__(self):
        return self.role_name
    
class Department(models.Model):
    department_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    department_name = models.CharField("Department Name", max_length=250, blank=False)

    def __str__(self):
        return self.department_name
    
class Group(models.Model):
    group_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    group_name = models.CharField("Group Name", max_length=250, blank=False)

    def __str__(self):
        return self.group_name