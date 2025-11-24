from django.db.models import Q
from rest_framework import viewsets
from .models import MessageTemplate, SubjectTemplate
from .serializers import MessageTemplateSerializer, SubjectTemplateSerializer


class MessageTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search) |
                Q(industry__icontains=search)
            )
        
        # Industry filter
        industry = self.request.query_params.get('industry', None)
        if industry:
            queryset = queryset.filter(industry__icontains=industry)
        
        return queryset.order_by('-created_at')


class SubjectTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubjectTemplate.objects.all()
    serializer_class = SubjectTemplateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(content__icontains=search)
        
        return queryset.order_by('-created_at')

