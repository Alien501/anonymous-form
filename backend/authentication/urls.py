from django.urls import path
from .views import (
    ResendUserCodeAPI, api_root
)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('resend_code/', ResendUserCodeAPI.as_view(), name='resend-code'),
]
