from django.urls import path
from .views import GetFormByIdAPI, SubmitFormResponse, GetCSRFToken, AIFillFormAPI

urlpatterns = [
    path('forms/<uuid:form_id>/', GetFormByIdAPI.as_view(), name='get-form-by-id'),
    path('forms/submit', SubmitFormResponse.as_view(), name='submit-form'),
    path('forms/ai-fill', AIFillFormAPI.as_view(), name='ai-fill-form'),
    path('csrf-token/', GetCSRFToken.as_view(), name='get-csrf-token'),
]
