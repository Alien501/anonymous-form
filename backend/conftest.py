"""
Pytest configuration and fixtures for the entire test suite
"""
import pytest
from django.conf import settings
from rest_framework.test import APIClient
from authentication.models import User
from organisation.models import Role, Department, Group
from forms.models import Form, Questions, FormQuestion
import os

# Configure test settings
settings.ENVIRONMENT = 'development'
settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
settings.DEBUG = False  # Disable debug mode in tests

# Disable Django Debug Toolbar in tests
if 'debug_toolbar' in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS = [app for app in settings.INSTALLED_APPS if app != 'debug_toolbar']

if 'debug_toolbar.middleware.DebugToolbarMiddleware' in settings.MIDDLEWARE:
    settings.MIDDLEWARE = [mw for mw in settings.MIDDLEWARE if mw != 'debug_toolbar.middleware.DebugToolbarMiddleware']


@pytest.fixture
def api_client():
    """Return an API client for testing"""
    return APIClient()


@pytest.fixture
def test_password():
    """Return a test password"""
    return 'TestPass123!@#'


@pytest.fixture
def create_user(db, test_password):
    """Factory fixture to create test users"""
    def make_user(**kwargs):
        kwargs.setdefault('email', f'test{User.objects.count()}@example.com')
        kwargs.setdefault('first_name', 'Test')
        kwargs.setdefault('last_name', 'User')
        kwargs.setdefault('password', test_password)
        # Don't set is_verified - it should default to False
        
        user = User.objects.create_user(**kwargs)
        return user
    return make_user


@pytest.fixture
def user(create_user):
    """Create a single test user"""
    return create_user()


@pytest.fixture
def admin_user(db, test_password):
    """Create an admin user"""
    return User.objects.create_superuser(
        email='admin@example.com',
        password=test_password,
        first_name='Admin',
        last_name='User'
    )


@pytest.fixture
def role(db):
    """Create a test role"""
    return Role.objects.create(role_name='Test Role')


@pytest.fixture
def department(db):
    """Create a test department"""
    return Department.objects.create(department_name='Test Department')


@pytest.fixture
def group(db):
    """Create a test group"""
    return Group.objects.create(group_name='Test Group')


@pytest.fixture
def form(db, role, department, group):
    """Create a test form"""
    form = Form.objects.create(
        name='Test Form',
        enable=True
    )
    form.roles.add(role)
    form.department.add(department)
    form.group.add(group)
    return form


@pytest.fixture
def question_text(db):
    """Create a text question"""
    return Questions.objects.create(
        question='What is your name?',
        answer_type='text',
        required=True,
        min_len=1,
        max_len=100
    )


@pytest.fixture
def question_radio(db):
    """Create a radio question"""
    return Questions.objects.create(
        question='Select your gender',
        answer_type='radio',
        required=True,
        options='Male||Female||Other'
    )


@pytest.fixture
def question_checkbox(db):
    """Create a checkbox question"""
    return Questions.objects.create(
        question='Select your interests',
        answer_type='checkbox',
        required=False,
        options='Sports||Music||Reading||Gaming'
    )


@pytest.fixture
def form_with_questions(form, question_text, question_radio, question_checkbox):
    """Create a form with questions"""
    FormQuestion.objects.create(form=form, question=question_text, form_index=1)
    FormQuestion.objects.create(form=form, question=question_radio, form_index=2)
    FormQuestion.objects.create(form=form, question=question_checkbox, form_index=3)
    return form


@pytest.fixture(autouse=True)
def cleanup_media(settings):
    """Clean up media files after each test"""
    yield
    # Cleanup can be added here if needed
    pass

