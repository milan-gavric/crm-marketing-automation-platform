"""
Views for email sending functionality
"""
import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import SendEmailSerializer
from .services import get_nylas_service

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])  # Adjust permissions as needed
def send_email(request):
    """
    Send an email using Nylas
    
    POST /api/email/send/
    
    Request Body:
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
    
    Returns:
        200: Email sent successfully
        400: Invalid request data
        500: Server error or Nylas configuration issue
    """
    serializer = SendEmailSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {
                'success': False,
                'error': 'Invalid request data',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    validated_data = serializer.validated_data
    
    # Get Nylas service
    nylas_service = get_nylas_service()
    
    if not nylas_service:
        return Response(
            {
                'success': False,
                'error': 'Nylas service is not configured',
                'message': 'Please set NYLAS_API_KEY in environment variables.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    try:
        # Send email via Nylas
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
        
        return Response(
            {
                'success': True,
                'message': 'Email sent successfully',
                'data': result
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}", exc_info=True)
        return Response(
            {
                'success': False,
                'error': 'Failed to send email',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

