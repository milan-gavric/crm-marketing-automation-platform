"""
Serializers for email sending functionality
"""
from rest_framework import serializers


class SendEmailSerializer(serializers.Serializer):
    """
    Serializer for sending email via Nylas
    
    Validates the request payload for email sending endpoint
    """
    grant_id = serializers.CharField(
        required=True,
        help_text="Nylas grant ID (connected account ID)"
    )
    to = serializers.ListField(
        child=serializers.EmailField(),
        required=True,
        min_length=1,
        help_text="List of recipient email addresses"
    )
    subject = serializers.CharField(
        required=True,
        max_length=1000,
        help_text="Email subject"
    )
    body = serializers.CharField(
        required=True,
        help_text="Email body (HTML or plain text)"
    )
    cc = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        allow_empty=True,
        help_text="Optional list of CC email addresses"
    )
    bcc = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        allow_empty=True,
        help_text="Optional list of BCC email addresses"
    )
    reply_to = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        allow_empty=True,
        help_text="Optional list of reply-to email addresses"
    )
    body_type = serializers.ChoiceField(
        choices=[('html', 'HTML'), ('text', 'Plain Text')],
        default='html',
        required=False,
        help_text="Email body type: 'html' or 'text'"
    )

    def validate(self, data):
        """
        Additional validation for the email sending request
        """
        # Validate that at least one recipient is provided
        if not data.get('to'):
            raise serializers.ValidationError({
                'to': 'At least one recipient is required'
            })
        
        # Validate grant_id is provided
        if not data.get('grant_id'):
            raise serializers.ValidationError({
                'grant_id': 'Grant ID is required'
            })
        
        return data

