"""
URL routing for email sending endpoints
"""
from django.urls import path
from .views import send_email

app_name = 'send'

urlpatterns = [
    path('', send_email, name='send-email'),
]

