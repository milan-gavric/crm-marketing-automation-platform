from rest_framework import viewsets, serializers
from .models import Email
from .serializers import EmailSerializer


class EmailViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Email model CRUD operations
    """
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related('account')
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(email__icontains=search)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        if not serializer.validated_data.get('email'):
            raise serializers.ValidationError({'email': 'Email is required'})
        
        email_data = serializer.validated_data.copy()
        email_data['email'] = email_data['email'].lower()
        
        account_id = self.request.data.get('accountId')
        if account_id:
            email_data['account_id'] = account_id
        
        serializer.save(**email_data)

