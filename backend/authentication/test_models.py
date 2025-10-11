"""
Tests for authentication models
"""
import pytest
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from authentication.models import User, UserManager


@pytest.mark.django_db
class TestUserManager:
    """Test cases for UserManager"""
    
    def test_create_user(self):
        """Test creating a regular user"""
        email = 'test@example.com'
        password = 'testpass123'
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name='Test',
            last_name='User'
        )
        
        assert user.email == email
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert check_password(password, user.password)
        assert not user.is_staff
        assert not user.is_superuser
        assert user.code  # Should have generated code
    
    def test_create_user_without_email(self):
        """Test that creating user without email raises error"""
        with pytest.raises(ValueError, match='Users require an email field'):
            User.objects.create_user(
                email='',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        email = 'admin@example.com'
        password = 'adminpass123'
        user = User.objects.create_superuser(
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        
        assert user.email == email
        assert user.is_staff
        assert user.is_superuser
        assert check_password(password, user.password)
    
    def test_create_superuser_with_wrong_flags(self):
        """Test that creating superuser with is_staff=False raises error"""
        with pytest.raises(ValueError, match='Superuser must have is_staff=True'):
            User.objects.create_superuser(
                email='admin@example.com',
                password='adminpass123',
                is_staff=False
            )


@pytest.mark.django_db
class TestUserModel:
    """Test cases for User model"""
    
    def test_user_creation(self, create_user):
        """Test basic user creation"""
        user = create_user(
            email='newuser@example.com',
            first_name='New',
            last_name='User'
        )
        
        assert user.email == 'newuser@example.com'
        assert user.first_name == 'New'
        assert user.last_name == 'User'
        assert user.uuid
        assert not user.is_verified
        assert user.code
    
    def test_user_email_uniqueness(self, create_user):
        """Test that email must be unique"""
        create_user(email='same@example.com')
        
        with pytest.raises(IntegrityError):
            create_user(email='same@example.com')
    
    def test_user_code_generation(self, create_user):
        """Test that user code is generated"""
        user = create_user()
        
        assert user.code
        assert len(user.code) == 6
        assert user.code.isupper() or user.code.isdigit() or user.code.isalnum()
    
    def test_generate_user_code_method(self, user):
        """Test the generate_user_code method"""
        code = user.generate_user_code()
        
        assert code
        assert len(code) == 6
        assert all(c.isupper() or c.isdigit() for c in code)
    
    def test_get_name_with_last_name(self, create_user):
        """Test get_name method with full name"""
        user = create_user(first_name='John', last_name='Doe')
        
        assert user.get_name() == 'John Doe'
    
    def test_get_name_without_last_name(self, create_user):
        """Test get_name method with only first name"""
        user = create_user(first_name='John', last_name='')
        
        assert user.get_name() == 'John'
    
    def test_password_hashing_on_save(self, db):
        """Test that password is hashed when saving user"""
        user = User(
            email='hash@example.com',
            first_name='Hash',
            last_name='Test',
            password='plaintext123'
        )
        user.save()
        
        assert user.password.startswith('pbkdf2_sha256$')
        assert check_password('plaintext123', user.password)
    
    def test_user_string_representation(self, user):
        """Test user string representation"""
        # Default str method should use email or username
        assert str(user)
    
    def test_user_uuid_uniqueness(self, create_user):
        """Test that UUID is unique for each user"""
        user1 = create_user()
        user2 = create_user()
        
        assert user1.uuid != user2.uuid
    
    def test_user_with_role(self, create_user, role):
        """Test user with role assignment"""
        user = create_user()
        user.role = role
        user.save()
        
        assert user.role == role
        assert user.role.role_name == 'Test Role'
    
    def test_user_with_department(self, create_user, department):
        """Test user with department assignment"""
        user = create_user()
        user.department = department
        user.save()
        
        assert user.department == department
        assert user.department.department_name == 'Test Department'
    
    def test_user_with_group(self, create_user, group):
        """Test user with group assignment"""
        user = create_user()
        user.group = group
        user.save()
        
        assert user.group == group
        assert user.group.group_name == 'Test Group'
    
    def test_send_user_code_method(self, user, mailoutbox):
        """Test sending user code via email"""
        user.send_user_code()
        
        # Check that email was sent
        assert len(mailoutbox) == 1
        email = mailoutbox[0]
        
        assert email.subject == 'Your User Code'
        assert user.email in email.to
        assert user.code in email.body or user.code in str(email.alternatives)

