"""
Tests for forms serializers
"""
import pytest
from forms.serializers import QuestionsSerializer, FormQuestionSerializer, FormSerializer
from forms.models import FormQuestion


@pytest.mark.django_db
class TestQuestionsSerializer:
    """Test cases for QuestionsSerializer"""
    
    def test_serialize_text_question(self, question_text):
        """Test serializing a text question"""
        serializer = QuestionsSerializer(question_text)
        data = serializer.data
        
        assert data['id'] == str(question_text.id)
        assert data['question'] == question_text.question
        assert data['answer_type'] == 'text'
        assert data['required'] == True
        assert data['min_len'] == 1
        assert data['max_len'] == 100
    
    def test_serialize_radio_question(self, question_radio):
        """Test serializing a radio question"""
        serializer = QuestionsSerializer(question_radio)
        data = serializer.data
        
        assert data['answer_type'] == 'radio'
        assert data['options'] == 'Male||Female||Other'
    
    def test_serialize_checkbox_question(self, question_checkbox):
        """Test serializing a checkbox question"""
        serializer = QuestionsSerializer(question_checkbox)
        data = serializer.data
        
        assert data['answer_type'] == 'checkbox'
        assert data['options'] is not None


@pytest.mark.django_db
class TestFormQuestionSerializer:
    """Test cases for FormQuestionSerializer"""
    
    def test_serialize_form_question(self, form, question_text):
        """Test serializing a form question"""
        fq = FormQuestion.objects.create(
            form=form,
            question=question_text,
            form_index=1
        )
        
        serializer = FormQuestionSerializer(fq)
        data = serializer.data
        
        assert data['id'] == str(fq.id)
        assert data['form_index'] == 1
        assert 'question' in data
        assert data['question']['id'] == str(question_text.id)


@pytest.mark.django_db
class TestFormSerializer:
    """Test cases for FormSerializer"""
    
    def test_serialize_form(self, form_with_questions):
        """Test serializing a form with questions"""
        serializer = FormSerializer(form_with_questions)
        data = serializer.data
        
        assert data['id'] == str(form_with_questions.id)
        assert data['name'] == form_with_questions.name
        assert 'form_questions' in data
        assert len(data['form_questions']) == 3
    
    def test_form_questions_ordering(self, form_with_questions):
        """Test that form questions are ordered correctly"""
        serializer = FormSerializer(form_with_questions)
        data = serializer.data
        
        questions = data['form_questions']
        indices = [q['form_index'] for q in questions]
        
        assert indices == sorted(indices)
    
    def test_serialize_empty_form(self, form):
        """Test serializing a form without questions"""
        serializer = FormSerializer(form)
        data = serializer.data
        
        assert data['id'] == str(form.id)
        assert data['name'] == form.name
        assert data['form_questions'] == []

