"""
Tests for authentication views and APIs
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestResendUserCodeAPI:
    """Test cases for ResendUserCodeAPI"""
    
    def test_resend_code_success(self, api_client, user, mailoutbox):
        """Test successfully resending user code"""
        url = '/api/resend_code/'
        response = api_client.get(url, {'email': user.email})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == 'User code sent to your email'
        
        # Check email was sent
        assert len(mailoutbox) == 1
        assert mailoutbox[0].to[0] == user.email
    
    def test_resend_code_user_not_found(self, api_client):
        """Test resending code for non-existent user"""
        url = '/api/resend_code/'
        response = api_client.get(url, {'email': 'nonexistent@example.com'})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['detail'] == 'User does not exist'
    
    def test_resend_code_no_email(self, api_client):
        """Test resending code without email parameter"""
        url = '/api/resend_code/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_resend_code_empty_email(self, api_client):
        """Test resending code with empty email"""
        url = '/api/resend_code/'
        response = api_client.get(url, {'email': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAPIRoot:
    """Test cases for API root endpoint"""
    
    def test_api_root(self, api_client):
        """Test API root returns available endpoints"""
        url = '/api/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'authentication' in response.data
        assert 'admin' in response.data
        assert 'message' in response.data

