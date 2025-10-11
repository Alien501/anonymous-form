"""
Tests for forms models
"""
import pytest
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from forms.models import Form, Questions, FormQuestion, FormResponse, FormUser


@pytest.mark.django_db
class TestFormModel:
    """Test cases for Form model"""
    
    def test_form_creation(self, db, role, department, group):
        """Test creating a form"""
        form = Form.objects.create(
            name='Test Form',
            enable=True
        )
        form.roles.add(role)
        form.department.add(department)
        form.group.add(group)
        
        assert form.name == 'Test Form'
        assert form.enable
        assert form.id
        assert str(form) == 'Test Form'
        assert form.roles.count() == 1
        assert form.department.count() == 1
        assert form.group.count() == 1
    
    def test_form_timestamps(self, form):
        """Test that form has timestamps"""
        assert form.created_at
        assert form.updated_at
    
    def test_disabled_form(self, db):
        """Test creating a disabled form"""
        form = Form.objects.create(
            name='Disabled Form',
            enable=False
        )
        
        assert not form.enable


@pytest.mark.django_db
class TestQuestionsModel:
    """Test cases for Questions model"""
    
    def test_text_question_creation(self, db):
        """Test creating a text question"""
        question = Questions.objects.create(
            question='What is your name?',
            answer_type='text',
            required=True,
            min_len=1,
            max_len=100
        )
        
        assert question.question == 'What is your name?'
        assert question.answer_type == 'text'
        assert question.required
        assert question.min_len == 1
        assert question.max_len == 100
        assert str(question) == 'What is your name?'
    
    def test_radio_question_with_options(self, db):
        """Test creating a radio question with options"""
        question = Questions.objects.create(
            question='Select gender',
            answer_type='radio',
            options='Male||Female||Other'
        )
        
        assert question.answer_type == 'radio'
        assert question.options == 'Male||Female||Other'
        assert '||' in question.options
    
    def test_checkbox_question(self, db):
        """Test creating a checkbox question"""
        question = Questions.objects.create(
            question='Select interests',
            answer_type='checkbox',
            options='Sports||Music||Reading'
        )
        
        assert question.answer_type == 'checkbox'
        assert question.options
    
    def test_file_question(self, db):
        """Test creating a file upload question"""
        question = Questions.objects.create(
            question='Upload your document',
            answer_type='file',
            file_type='application/pdf',
            max_len=5  # 5 MB
        )
        
        assert question.answer_type == 'file'
        assert question.file_type == 'application/pdf'
    
    def test_number_question(self, db):
        """Test creating a number question"""
        question = Questions.objects.create(
            question='Enter your age',
            answer_type='number',
            min_len=1,
            max_len=150
        )
        
        assert question.answer_type == 'number'
    
    def test_boolean_question(self, db):
        """Test creating a boolean question"""
        question = Questions.objects.create(
            question='Do you agree?',
            answer_type='boolean'
        )
        
        assert question.answer_type == 'boolean'
    
    def test_question_timestamps(self, question_text):
        """Test that question has timestamps"""
        assert question_text.created_at
        assert question_text.updated_at


@pytest.mark.django_db
class TestFormQuestionModel:
    """Test cases for FormQuestion model"""
    
    def test_form_question_creation(self, form, question_text):
        """Test creating a form question"""
        fq = FormQuestion.objects.create(
            form=form,
            question=question_text,
            form_index=1
        )
        
        assert fq.form == form
        assert fq.question == question_text
        assert fq.form_index == 1
        assert str(fq) == f'{form} - {question_text}'
    
    def test_form_question_auto_index(self, form, question_text, question_radio):
        """Test that form_index is auto-generated"""
        fq1 = FormQuestion.objects.create(form=form, question=question_text)
        fq2 = FormQuestion.objects.create(form=form, question=question_radio)
        
        assert fq1.form_index == 1
        assert fq2.form_index == 2
    
    def test_form_question_manual_index(self, form, question_text):
        """Test setting form_index manually"""
        fq = FormQuestion.objects.create(
            form=form,
            question=question_text,
            form_index=5
        )
        
        assert fq.form_index == 5
    
    def test_multiple_questions_same_form(self, form_with_questions):
        """Test adding multiple questions to a form"""
        questions = FormQuestion.objects.filter(form=form_with_questions)
        
        assert questions.count() == 3
        assert list(questions.values_list('form_index', flat=True).order_by('form_index')) == [1, 2, 3]


@pytest.mark.django_db
class TestFormUserModel:
    """Test cases for FormUser model"""
    
    def test_form_user_creation(self, user, form):
        """Test creating a FormUser entry"""
        form_user = FormUser.objects.create(
            user=user,
            form=form
        )
        
        assert form_user.user == user
        assert form_user.form == form
        assert form_user.created_at
        assert str(form_user) == f'{user.get_name()} - {form.name}'
    
    def test_form_user_uniqueness(self, user, form):
        """Test that a user can be tracked for a form"""
        FormUser.objects.create(user=user, form=form)
        
        # Should be able to query it
        exists = FormUser.objects.filter(user=user, form=form).exists()
        assert exists


@pytest.mark.django_db
class TestFormResponseModel:
    """Test cases for FormResponse model"""
    
    def test_form_response_creation(self, form, question_text, question_radio):
        """Test creating a form response"""
        response_data = {
            str(question_text.id): {
                'question': question_text.question,
                'answer_type': 'text',
                'value': 'John Doe',
                'required': True
            },
            str(question_radio.id): {
                'question': question_radio.question,
                'answer_type': 'radio',
                'value': 'Male',
                'required': True
            }
        }
        
        form_response = FormResponse.objects.create(
            form=form,
            response=response_data
        )
        
        assert form_response.form == form
        assert form_response.response == response_data
        assert form_response.id
        assert form_response.created_at
    
    def test_form_response_json_field(self, form):
        """Test that response field stores JSON"""
        complex_response = {
            'q1': {'value': 'text answer'},
            'q2': {'value': ['option1', 'option2']},
            'q3': {'value': True},
            'q4': {'value': 42}
        }
        
        form_response = FormResponse.objects.create(
            form=form,
            response=complex_response
        )
        
        # Retrieve and verify
        saved_response = FormResponse.objects.get(id=form_response.id)
        assert saved_response.response == complex_response
    
    def test_form_response_with_file_data(self, form, db):
        """Test form response with file upload data"""
        response_data = {
            'file_question': {
                'answer_type': 'file',
                'value': {
                    'file_path': 'form_uploads/test/file.pdf',
                    'original_name': 'document.pdf'
                }
            }
        }
        
        form_response = FormResponse.objects.create(
            form=form,
            response=response_data
        )
        
        assert 'file_path' in form_response.response['file_question']['value']

