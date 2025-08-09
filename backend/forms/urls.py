from django.urls import path
from .views import GetFormByIdAPI

urlpatterns = [
    path('forms/<uuid:form_id>/', GetFormByIdAPI.as_view(), name='get-form-by-id'),
]
