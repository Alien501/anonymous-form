"""
Tests for authentication serializers
"""
import pytest
from authentication.serializers import UserSerializer
from authentication.models import User


@pytest.mark.django_db
class TestUserSerializer:
    """Test cases for UserSerializer"""
    
    def test_valid_user_serializer(self):
        """Test serializer with valid data"""
        data = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        }
        
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        assert user.email == data['email']
        assert user.first_name == data['first_name']
        assert user.last_name == data['last_name']
        assert user.check_password(data['password'])
    
    def test_password_mismatch(self):
        """Test serializer with mismatched passwords"""
        data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'StrongPass123!',
            'password_confirm': 'DifferentPass123!'
        }
        
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
    
    def test_weak_password(self):
        """Test serializer with weak password"""
        data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '123',
            'password_confirm': '123'
        }
        
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
    
    def test_missing_required_fields(self):
        """Test serializer with missing required fields"""
        data = {
            'email': 'test@example.com'
        }
        
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'first_name' in serializer.errors
        assert 'last_name' in serializer.errors
        assert 'password' in serializer.errors
    
    def test_invalid_email(self):
        """Test serializer with invalid email"""
        data = {
            'email': 'not-an-email',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        }
        
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

