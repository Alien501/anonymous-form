from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Form
from .serializers import FormSerializer

# Create your views here.
class GetFormByIdAPI(APIView):
    def get(self, request, form_id):
        try:
            form = get_object_or_404(Form, id=form_id, enable=True)
            serializer = FormSerializer(form)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Form not found or invalid form ID'}, 
                status=status.HTTP_404_NOT_FOUND
            )
