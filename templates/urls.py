from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageTemplateViewSet, SubjectTemplateViewSet

router = DefaultRouter()
router.register(r'message', MessageTemplateViewSet, basename='message-template')
router.register(r'subject', SubjectTemplateViewSet, basename='subject-template')

urlpatterns = [
    path('', include(router.urls)),
]

