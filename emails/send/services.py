"""
Nylas email sending service
"""
import logging
from django.conf import settings
from nylas import Client
from typing import List, Optional

logger = logging.getLogger(__name__)


class NylasEmailService:
    """
    Service class to handle email sending via Nylas API
    """
    
    def __init__(self):
        self.api_key = settings.NYLAS_API_KEY
        self.api_uri = settings.NYLAS_API_URI
        
        if not self.api_key:
            raise ValueError("NYLAS_API_KEY is not configured in settings")
        
        # Initialize Nylas client
        self.client = Client(
            api_key=self.api_key,
            api_uri=self.api_uri
        )
    
    def send_email(
        self,
        grant_id: str,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[List[str]] = None,
        body_type: str = 'html'
    ) -> dict:
        """
        Send an email using Nylas API
        
        Args:
            grant_id: Nylas grant ID (connected account ID)
            to: List of recipient email addresses
            subject: Email subject
            body: Email body (HTML or plain text)
            cc: Optional list of CC email addresses
            bcc: Optional list of BCC email addresses
            reply_to: Optional list of reply-to email addresses
            body_type: 'html' or 'text' (default: 'html')
        
        Returns:
            dict: Response from Nylas API containing message_id, thread_id, etc.
        
        Raises:
            Exception: If email sending fails
        """
        try:
            # Prepare recipients
            to_list = [{"email": email} for email in to]
            
            # Prepare draft request body
            draft_body = {
                "to": to_list,
                "subject": subject,
                "body": body,
            }
            
            # Add optional fields
            if cc:
                draft_body["cc"] = [{"email": email} for email in cc]
            if bcc:
                draft_body["bcc"] = [{"email": email} for email in bcc]
            if reply_to:
                draft_body["reply_to"] = [{"email": email} for email in reply_to]
            
            # Create draft
            draft = self.client.drafts.create(
                grant_id,
                request_body=draft_body
            )
            
            # Send the email
            sent_message = self.client.drafts.send(
                grant_id,
                draft.id
            )
            
            logger.info(f"Email sent successfully. Message ID: {sent_message.get('id', 'N/A')}")
            
            return {
                'success': True,
                'message_id': sent_message.get('id'),
                'thread_id': sent_message.get('thread_id'),
                'grant_id': grant_id
            }
            
        except Exception as e:
            logger.error(f"Error sending email via Nylas: {str(e)}")
            raise Exception(f"Failed to send email: {str(e)}")


def get_nylas_service() -> Optional[NylasEmailService]:
    """
    Factory function to get NylasEmailService instance
    
    Returns:
        NylasEmailService instance or None if configuration is missing
    """
    try:
        return NylasEmailService()
    except ValueError as e:
        logger.error(str(e))
        return None

