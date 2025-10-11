"""
Tests for forms views and APIs
"""
import pytest
import json
from django.urls import reverse
from rest_framework import status
from forms.models import FormResponse, FormUser


@pytest.mark.django_db
class TestGetFormByIdAPI:
    """Test cases for GetFormByIdAPI"""
    
    def test_get_form_success(self, api_client, form_with_questions):
        """Test successfully retrieving a form"""
        url = f'/api/forms/{form_with_questions.id}/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(form_with_questions.id)
        assert response.data['name'] == form_with_questions.name
        assert 'form_questions' in response.data
        assert len(response.data['form_questions']) == 3
    
    def test_get_disabled_form(self, api_client, form):
        """Test retrieving a disabled form returns 404"""
        form.enable = False
        form.save()
        
        url = f'/api/forms/{form.id}/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_nonexistent_form(self, api_client):
        """Test retrieving non-existent form"""
        url = '/api/forms/00000000-0000-0000-0000-000000000000/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_form_questions_ordering(self, api_client, form_with_questions):
        """Test that form questions are ordered by form_index"""
        url = f'/api/forms/{form_with_questions.id}/'
        response = api_client.get(url)
        
        questions = response.data['form_questions']
        indices = [q['form_index'] for q in questions]
        
        assert indices == sorted(indices)


@pytest.mark.django_db
class TestGetCSRFToken:
    """Test cases for GetCSRFToken API"""
    
    def test_get_csrf_token(self, api_client):
        """Test getting CSRF token"""
        url = '/api/csrf-token/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'csrf_token' in response.data
        assert response.data['csrf_token']


@pytest.mark.django_db
class TestSubmitFormResponse:
    """Test cases for SubmitFormResponse API"""
    
    def test_submit_form_success(self, api_client, user, form_with_questions):
        """Test successfully submitting a form"""
        responses = {
            str(form_with_questions.formquestion_set.all()[0].question.id): {
                'question': 'What is your name?',
                'answer_type': 'text',
                'value': 'John Doe',
                'required': True
            },
            str(form_with_questions.formquestion_set.all()[1].question.id): {
                'question': 'Select your gender',
                'answer_type': 'radio',
                'value': 'Male',
                'required': True
            }
        }
        
        data = {
            'user_code': user.code,
            'formId': str(form_with_questions.id),
            'responses': json.dumps(responses)
        }
        
        url = '/api/forms/submit/'
        response = api_client.post(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'response_id' in response.data
        assert response.data['message'] == 'Form submitted successfully!'
        
        # Verify FormResponse was created
        assert FormResponse.objects.filter(form=form_with_questions).exists()
        
        # Verify FormUser was created
        assert FormUser.objects.filter(user=user, form=form_with_questions).exists()
    
    def test_submit_form_without_user_code(self, api_client, form_with_questions):
        """Test submitting form without user code"""
        data = {
            'formId': str(form_with_questions.id),
            'responses': json.dumps({})
        }
        
        url = '/api/forms/submit/'
        response = api_client.post(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'User code is required' in response.data['message']
    
    def test_submit_form_invalid_user_code(self, api_client, form_with_questions):
        """Test submitting form with invalid user code"""
        # Need to provide some responses to pass that validation
        responses = {
            'some_question': {
                'answer_type': 'text',
                'value': 'some answer'
            }
        }
        
        data = {
            'user_code': 'INVALID',
            'formId': str(form_with_questions.id),
            'responses': json.dumps(responses)
        }
        
        url = '/api/forms/submit/'
        response = api_client.post(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Invalid user code' in response.data['message']
    
    def test_submit_form_without_form_id(self, api_client, user):
        """Test submitting form without form ID"""
        data = {
            'user_code': user.code,
            'responses': json.dumps({})
        }
        
        url = '/api/forms/submit/'
        response = api_client.post(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Form ID is required' in response.data['message']
    
    def test_submit_form_disabled_form(self, api_client, user, form):
        """Test submitting to disabled form"""
        form.enable = False
        form.save()
        
        data = {
            'user_code': user.code,
            'formId': str(form.id),
            'responses': json.dumps({'q1': 'answer'})
        }
        
        url = '/api/forms/submit/'
        response = api_client.post(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Form not found or disabled' in response.data['message']
    
    def test_submit_form_twice(self, api_client, user, form_with_questions):
        """Test that user cannot submit same form twice"""
        responses = {
            str(form_with_questions.formquestion_set.all()[0].question.id): {
                'answer_type': 'text',
                'value': 'Answer'
            }
        }
        
        data = {
            'user_code': user.code,
            'formId': str(form_with_questions.id),
            'responses': json.dumps(responses)
        }
        
        url = '/api/forms/submit/'
        
        # First submission
        response1 = api_client.post(url, data, format='multipart')
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Second submission should fail
        response2 = api_client.post(url, data, format='multipart')
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert 'already submitted' in response2.data['message']
    
    def test_submit_form_without_responses(self, api_client, user, form_with_questions):
        """Test submitting form without responses"""
        data = {
            'user_code': user.code,
            'formId': str(form_with_questions.id),
            'responses': '{}'
        }
        
        url = '/api/forms/submit/'
        response = api_client.post(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Form responses are required' in response.data['message']


@pytest.mark.django_db
class TestAIFillFormAPI:
    """Test cases for AIFillFormAPI"""
    
    def test_ai_fill_form_missing_form_id(self, api_client):
        """Test AI fill without form ID"""
        data = {
            'userInput': 'Fill this form for me'
        }
        
        url = '/api/forms/ai-fill/'
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Form ID is required' in response.data['error']
    
    def test_ai_fill_form_missing_user_input(self, api_client, form):
        """Test AI fill without user input"""
        data = {
            'formId': str(form.id)
        }
        
        url = '/api/forms/ai-fill/'
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'User input is required' in response.data['error']
    
    def test_ai_fill_form_nonexistent_form(self, api_client):
        """Test AI fill with non-existent form"""
        data = {
            'formId': '00000000-0000-0000-0000-000000000000',
            'userInput': 'Fill this form'
        }
        
        url = '/api/forms/ai-fill/'
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Form not found or disabled' in response.data['error']
    
    def test_ai_fill_form_no_questions(self, api_client, form):
        """Test AI fill with form that has no questions"""
        data = {
            'formId': str(form.id),
            'userInput': 'Fill this form'
        }
        
        url = '/api/forms/ai-fill/'
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'No questions found' in response.data['error']

