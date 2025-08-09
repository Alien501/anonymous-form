import logging
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from .models import Form, FormResponse, FormUser
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
            user_code = request.data.get('user_code')
            form_id = request.data.get('formId')
            responses = request.data.get('responses', {})
            
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