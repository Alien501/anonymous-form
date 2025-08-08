from django.db import models

from organisation.models import *

import uuid

# Create your models here.
class Form(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField("Form Name", max_length=255)
    roles = models.ManyToManyField(Role)
    department = models.ManyToManyField(Department)
    group = models.ManyToManyField(Group)
    