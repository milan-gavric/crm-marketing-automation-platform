from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Email
from .serializers import EmailSerializer, SendEmailSerializer
from .services import get_nylas_service
import logging

logger = logging.getLogger(__name__)


class EmailViewSet(viewsets.ModelViewSet):
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

    @action(detail=False, methods=['post'])
    def send(self, request):
        """
        Send an email using Nylas
        Expected payload:
        {
            "grant_id": "nylas_grant_id",
            "to": ["recipient@example.com"],
            "subject": "Email Subject",
            "body": "<html>Email body</html>",
            "cc": ["cc@example.com"],  // optional
            "bcc": ["bcc@example.com"],  // optional
            "reply_to": ["reply@example.com"],  // optional
            "body_type": "html"  // optional, default: "html"
        }
        """
        serializer = SendEmailSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid request data', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        
        # Get Nylas service
        nylas_service = get_nylas_service()
        
        if not nylas_service:
            return Response(
                {'error': 'Nylas service is not configured. Please set NYLAS_API_KEY in environment variables.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            # Send email
            result = nylas_service.send_email(
                grant_id=validated_data['grant_id'],
                to=validated_data['to'],
                subject=validated_data['subject'],
                body=validated_data['body'],
                cc=validated_data.get('cc'),
                bcc=validated_data.get('bcc'),
                reply_to=validated_data.get('reply_to'),
                body_type=validated_data.get('body_type', 'html')
            )
            
            return Response({
                'success': True,
                'message': 'Email sent successfully',
                'data': result
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return Response(
                {'error': 'Failed to send email', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

