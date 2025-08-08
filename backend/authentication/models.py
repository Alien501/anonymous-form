from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework import status

from utils.send_mail import send_email, send_html_email

import uuid, jwt, string, random

from organisation.models import *

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    username = None

    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('First Name',max_length=255, blank=False)
    last_name = models.CharField('Last Name',max_length=255, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=False)
    
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name='user_role',null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='user_department',null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='user_group',null=True, blank=True)
    
    code = models.CharField("User Code", max_length=100, default="", blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def clean(self):
        if self.code.strip() == "":
            self.code = self.generate_user_code()
    
    def generate_user_code(self, *args, **kwargs):
        length = 6
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))

    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().clean()
        super().save(*args, **kwargs)

    def get_name(self):
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name}'
    
    # TODO: Rename: send_user_code
    def send_verification_mail(self):
        verification_token = get_random_string(length=8)
        startingcontent = f"Greetings! <b>{self.first_name}</b>,\n\n Thank you for showing interest in our application. Please click on the confirmation link given below to finish setting up your account."
        endingcontent = f"If you have any general questions for us please do not hesitate to contact us. \n\nWe look forward to having you on board!\n\nWarm Regards,\nTeam App Name"
        link = f"{settings.VERIFICATION_URL}?token={verification_token}&email={self.email}"
        linkcontent = "Click this link to verify your email"
        subject = "Email Verification"
        to_email = self.email
        
        verification, created = VerificationCode.objects.get_or_create(user=self)
        verification.code = verification_token
        verification.save()
        
        send_html_email(
            subject=subject, 
            to_email=to_email, 
            context={
                "startingcontent": startingcontent, 
                "endingcontent": endingcontent, 
                "link": link, 
                "linkcontent": linkcontent,
                "user_name": self.first_name,
                "app_name": "App Name"
            },
            template_name="email/verification_email.html"
        )