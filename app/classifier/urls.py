# classifier/urls.py
from django.urls import path
from .views import SMSClassificationView

urlpatterns = [
    path('predict/', SMSClassificationView.as_view(), name='sms_classification'),
]
