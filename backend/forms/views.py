import logging
import os
import uuid
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.conf import settings
import json
import google.generativeai as genai
from decouple import config

from .models import Form, FormResponse, FormUser, FormQuestion
from .serializers import FormSerializer
from authentication.models import User

# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.
class GetFormByIdAPI(APIView):
    def get(self, request, form_id):
        try:
            form = get_object_or_404(Form, id=form_id, enable=True)
            serializer = FormSerializer(form)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching form {form_id}: {str(e)}")
            return Response(
                {'error': 'Form not found or invalid form ID'}, 
                status=status.HTTP_404_NOT_FOUND
            )

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({
            'csrf_token': csrf_token
        }, status=status.HTTP_200_OK)

class SubmitFormResponse(APIView):
    def post(self, request):
        try:
            print("files", request.FILES)
            user_code = request.data.get('user_code')
            form_id = request.data.get('formId')
            responses_data = request.data.get('responses', '{}')
            
            # Parse responses JSON
            try:
                responses = json.loads(responses_data) if isinstance(responses_data, str) else responses_data
            except json.JSONDecodeError:
                logger.error("Invalid JSON in responses data")
                return Response(
                    {"message": "Invalid form data format!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            logger.info(f"Form submission attempt - User: {user_code}, Form: {form_id}")
            
            if not user_code:
                logger.warning(f"Form submission failed - Missing user code for form {form_id}")
                return Response(
                    {
                        "message": "User code is required!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not form_id:
                logger.warning("Form submission failed - Missing form ID")
                return Response(
                    {
                        "message": "Form ID is required!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not responses:
                logger.warning(f"Form submission failed - Missing responses for form {form_id}")
                return Response(
                    {
                        "message": "Form responses are required!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate user code
            try:
                user = User.objects.get(code=user_code)
                logger.info(f"User validated successfully: {user.email}")
            except User.DoesNotExist:
                logger.warning(f"Form submission failed - Invalid user code: {user_code}")
                return Response(
                    {
                        "message": "Invalid user code!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if form exists and is enabled
            try:
                form = Form.objects.get(id=form_id, enable=True)
                logger.info(f"Form validated successfully: {form.name}")
            except Form.DoesNotExist:
                logger.warning(f"Form submission failed - Form not found or disabled: {form_id}")
                return Response(
                    {
                        "message": "Form not found or disabled!"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if user has already submitted this form using FormUser
            existing_form_user = FormUser.objects.filter(
                user=user,
                form=form
            ).first()
            
            if existing_form_user:
                logger.warning(f"Form submission failed - User {user_code} already submitted form {form_id}")
                return Response(
                    {
                        "message": "You have already submitted this form!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process file uploads
            for question_id, response_data in responses.items():
                if response_data.get('answer_type') == 'file' and response_data.get('value'):
                    file_key = f'file_{question_id}'
                    if file_key in request.FILES:
                        uploaded_file = request.FILES[file_key]
                        
                        # Create upload directory if it doesn't exist
                        upload_dir = os.path.join(settings.MEDIA_ROOT, 'form_uploads', str(form_id), str(user.id))
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        # Generate unique filename
                        file_extension = os.path.splitext(uploaded_file.name)[1]
                        unique_filename = f"{uuid.uuid4()}{file_extension}"
                        file_path = os.path.join(upload_dir, unique_filename)
                        
                        # Save the file
                        with open(file_path, 'wb+') as destination:
                            for chunk in uploaded_file.chunks():
                                destination.write(chunk)
                        
                        # Update response with file path
                        relative_path = os.path.join('form_uploads', str(form_id), str(user.id), unique_filename)
                        response_data['value']['file_path'] = relative_path
                        response_data['value']['original_name'] = uploaded_file.name
            
            # Store the form response and create FormUser entry
            print(responses)
            with transaction.atomic():
                
                form_response = FormResponse.objects.create(
                    form=form,
                    response=responses
                )
                
                FormUser.objects.create(
                    user=user,
                    form=form
                )
                
                logger.info(f"Form submission successful - User: {user_code}, Form: {form_id}, Response ID: {form_response.id}")
            
            return Response(
                {
                    "message": "Form submitted successfully!",
                    "response_id": str(form_response.id)
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"Form submission error: {str(e)}", exc_info=True)
            return Response(
                {
                    "message": "An error occurred while submitting the form.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AIFillFormAPI(APIView):
    def post(self, request):
        try:
            form_id = request.data.get('formId')
            user_input = request.data.get('userInput', '').strip()
            
            if not form_id:
                return Response(
                    {"error": "Form ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not user_input:
                return Response(
                    {"error": "User input is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                form = Form.objects.get(id=form_id, enable=True)
            except Form.DoesNotExist:
                return Response(
                    {"error": "Form not found or disabled"},
                    status=status.HTTP_404_NOT_FOUND
                )
            form_questions = FormQuestion.objects.filter(form=form).select_related('question').order_by('form_index')
            
            if not form_questions.exists():
                return Response(
                    {"error": "No questions found for this form"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            questions_data = []
            for fq in form_questions:
                q = fq.question
                question_info = {
                    'id': str(q.id),
                    'question': q.question,
                    'answer_type': q.answer_type,
                    'required': q.required,
                }
                
                if q.options:
                    question_info['options'] = [opt.strip() for opt in q.options.split('||')]
                
                questions_data.append(question_info)
            
            api_key = config('GEMINI_API_KEY')
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""You are a helpful AI assistant that fills out forms based on user input. 
            
The user has provided the following input:
"{user_input}"

Based on this input, please fill out the following form. Return ONLY a valid JSON object with question IDs as keys and appropriate values.

Form Questions:
{json.dumps(questions_data, indent=2)}

Instructions:
1. For 'text' type questions: provide a string value
2. For 'number' type questions: provide a numeric value
3. For 'boolean' type questions: provide true or false
4. For 'radio' type questions: select ONE option EXACTLY as shown in the options array (including any spaces)
5. For 'checkbox' type questions: provide an array with EXACT option values from the options array (including any spaces)
6. For 'select' type questions: select ONE option EXACTLY as shown in the options array (including any spaces)
7. For 'file' type questions: set the value to null (files cannot be auto-filled)
8. If the user input doesn't provide information for a question, use null for non-required fields or make a reasonable inference for required fields
9. Ensure all required fields have values (not null)
10. IMPORTANT: For radio, checkbox, and select - copy the option values EXACTLY as they appear in the options array, do not trim spaces or modify them

Return ONLY a JSON object in this exact format:
{{
  "question_id_1": "value1",
  "question_id_2": 123,
  "question_id_3": true,
  "question_id_4": ["option1", "option2"],
  ...
}}

Do not include any markdown, explanations, or additional text. Only return the raw JSON object."""

            response = model.generate_content(prompt)
            
            try:
                response_text = response.text.strip()
                
                if response_text.startswith('```'):
                    response_text = response_text.split('```')[1]
                    if response_text.startswith('json'):
                        response_text = response_text[4:].strip()
                
                ai_responses = json.loads(response_text)
                
                logger.info(f"AI generated responses for form {form_id}: {ai_responses}")
                
                return Response({
                    "success": True,
                    "responses": ai_responses
                }, status=status.HTTP_200_OK)
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response: {str(e)}")
                logger.error(f"Raw response: {response.text}")
                return Response(
                    {"error": "Failed to parse AI response", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        except Exception as e:
            logger.error(f"AI form fill error: {str(e)}", exc_info=True)
            return Response(
                {"error": "An error occurred while processing your request", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

'''
    {
    "user_code": "123453rt",
    "data": {
        "formId": "1f87b512-3c97-4116-9a94-a3eb43f34a82",
        "formName": "Hostel Food Feedback",
        "responses": {
        "09728472-c6b4-464b-bfa1-1f78f64b7ba8": {
            "question": "Hostel Name",
            "answer_type": "text",
            "value": "Habitat",
            "required": true
        },
        "fd426383-5916-468b-900c-eb95c2cfba3c": {
            "question": "What is your gender?",
            "answer_type": "radio",
            "value": "Male ",
            "required": true
        },
        "359e5db5-4341-457d-8657-5bd6b74d695f": {
            "question": "Veg Or Non-Veg?",
            "answer_type": "select",
            "value": "Veg ",
            "required": false
        },
        "e3985a43-2920-4769-8c5e-470c9759ff95": {
            "question": "What would you like to improve",
            "answer_type": "checkbox",
            "value": [" Option 2 ", "Option 1 "],
            "required": true
        },
        "87ceab03-9f0c-43d5-b54e-0804849f22ab": {
            "question": "Feedback",
            "answer_type": "text",
            "value": "Hello Worl",
            "required": true
        },
        "4d134ebe-eb65-48ac-a9a2-2808121f713e": {
            "question": "Is the food really good?",
            "answer_type": "boolean",
            "value": true,
            "required": true
        },
        "ac9c4c14-fa4d-49d7-be80-bb8bb6883f64": {
            "question": "Your rating?",
            "answer_type": "number",
            "value": 100,
            "required": false
        },
        "83abd06e-90a7-4fa1-b4be-c35152ff8545": {
            "question": "Image?",
            "answer_type": "file",
            "value": {
            "name": "0939cab7-f15e-4435-aab7-dcff3630e002.jpg",
            "size": 82509,
            "type": "image/jpeg",
            "lastModified": 1754171695699
            },
            "required": false
        }
        },
        "timestamp": "2025-08-09T11:56:29.941Z"
    }
    }

'''