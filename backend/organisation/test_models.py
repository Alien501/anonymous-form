"""
Tests for organisation models
"""
import pytest
from organisation.models import Role, Department, Group


@pytest.mark.django_db
class TestRoleModel:
    """Test cases for Role model"""
    
    def test_role_creation(self, db):
        """Test creating a role"""
        role = Role.objects.create(role_name='Test Role')
        
        assert role.role_name == 'Test Role'
        assert role.role_id
        assert str(role) == 'Test Role'
    
    def test_role_uuid_uniqueness(self, db):
        """Test that role_id is unique"""
        role1 = Role.objects.create(role_name='Role 1')
        role2 = Role.objects.create(role_name='Role 2')
        
        assert role1.role_id != role2.role_id


@pytest.mark.django_db
class TestDepartmentModel:
    """Test cases for Department model"""
    
    def test_department_creation(self, db):
        """Test creating a department"""
        dept = Department.objects.create(department_name='Engineering')
        
        assert dept.department_name == 'Engineering'
        assert dept.department_id
        assert str(dept) == 'Engineering'
    
    def test_department_uuid_uniqueness(self, db):
        """Test that department_id is unique"""
        dept1 = Department.objects.create(department_name='Dept 1')
        dept2 = Department.objects.create(department_name='Dept 2')
        
        assert dept1.department_id != dept2.department_id


@pytest.mark.django_db
class TestGroupModel:
    """Test cases for Group model"""
    
    def test_group_creation(self, db):
        """Test creating a group"""
        group = Group.objects.create(group_name='Test Group')
        
        assert group.group_name == 'Test Group'
        assert group.group_id
        assert str(group) == 'Test Group'
    
    def test_group_uuid_uniqueness(self, db):
        """Test that group_id is unique"""
        group1 = Group.objects.create(group_name='Group 1')
        group2 = Group.objects.create(group_name='Group 2')
        
        assert group1.group_id != group2.group_id

