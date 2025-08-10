from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from .authentication import IsAuthenticated


@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root - List all available endpoints
    """
    return Response({
        'authentication': {
            'resend_code': '/api/resend_code/',
        },
        'admin': '/admin/',
        'message': 'Welcome to the API! Visit any endpoint to test the browsable interface.',
    })


# Create your views here.
class ResendUserCodeAPI(APIView):
    def get(self, request):
        email = request.query_params.get('email', '')
        try:
            user = User.objects.get(email=email)
            user.send_user_code()
            return Response({'detail': 'User code sent to your email'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)