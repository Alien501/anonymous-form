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
            'register': '/api/register/',
            'login': '/api/login/',
            'verify': '/api/verify/',
            'resend_token': '/api/resend_token/',
            'forgot_password': '/api/forgot_password/',
            'profile': '/api/profile/',
            'logout': '/api/logout/',
        },
        'admin': '/admin/',
        'message': 'Welcome to the API! Visit any endpoint to test the browsable interface.',
    })


# Create your views here.
class ResendVerificationTokenAPI(APIView):
    def get(self, request):
        email = request.query_params.get('email', '')
        try:
            print(email)
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({'detail': 'User Already Verified'}, status=status.HTTP_400_BAD_REQUEST)
            user.send_verification_mail()
            return Response({'detail': 'Verification code sent to your email'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('token', domain=settings.COOKIE_DOMAIN)
        return response