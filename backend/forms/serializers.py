from rest_framework import serializers
from .models import Form, Questions, FormQuestion

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = [
            'id', 'question', 'required', 'answer_type', 
            'min_len', 'max_len', 'options', 'file_type',
        ]


class FormQuestionSerializer(serializers.ModelSerializer):
    question = QuestionsSerializer(read_only=True)
    
    class Meta:
        model = FormQuestion
        fields = ['id', 'question', 'form_index']


class FormSerializer(serializers.ModelSerializer):
    form_questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Form
        fields = [
            'id', 'name', 'form_questions'
        ]
    
    def get_form_questions(self, obj):
        # Get form questions ordered by form_index
        form_questions = obj.formquestion_set.all().order_by('form_index')
        return FormQuestionSerializer(form_questions, many=True).data


# class FormResponseSerializer(serializers.BaseSerializer)