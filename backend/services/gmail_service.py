from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import email
from datetime import datetime, timedelta
import os
import logging

logger = logging.getLogger(__name__)

class GmailService:
    def __init__(self, user):
        self.user = user
        self.service = self._build_service()
    
    def _build_service(self):
        """Build Gmail service with user credentials"""
        try:
            credentials = Credentials(
                token=self.user.gmail_access_token,
                refresh_token=self.user.gmail_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=os.getenv('GOOGLE_CLIENT_ID'),
                client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
            )
            
            # Refresh token if expired
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                
                # Update user's tokens
                self.user.gmail_access_token = credentials.token
                self.user.gmail_token_expiry = credentials.expiry
                self.user.updated_at = datetime.utcnow()
                from run import db
                db.session.commit()
            
            return build('gmail', 'v1', credentials=credentials)
        
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
            raise
    
    def get_unprocessed_emails(self, max_results=50):
        """Get unprocessed emails from Gmail inbox"""
        try:
            # Get emails from inbox (not including sent, spam, etc.)
            query = "in:inbox"
            
            # Get emails from the last 7 days to avoid processing too much history
            week_ago = datetime.utcnow() - timedelta(days=7)
            query += f" after:{week_ago.strftime('%Y/%m/%d')}"
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                try:
                    email_data = self._get_email_details(message['id'])
                    if email_data:
                        emails.append(email_data)
                except Exception as e:
                    logger.error(f"Failed to get details for message {message['id']}: {e}")
                    continue
            
            return emails
        
        except HttpError as error:
            logger.error(f"Gmail API error: {error}")
            raise
        except Exception as e:
            logger.error(f"Failed to get emails: {e}")
            raise
    
    def _get_email_details(self, message_id):
        """Get detailed information about a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            # Extract email details
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            date_str = next((h['value'] for h in headers if h['name'] == 'Date'), None)
            
            # Parse sender name and email
            sender_name, sender_email = self._parse_sender(sender)
            
            # Parse date
            received_at = self._parse_date(date_str) if date_str else datetime.utcnow()
            
            # Extract body
            body = self._extract_body(message['payload'])
            
            return {
                'gmail_id': message_id,
                'thread_id': message.get('threadId'),
                'subject': subject,
                'sender': sender_name,
                'sender_email': sender_email,
                'body': body,
                'snippet': message.get('snippet', ''),
                'received_at': received_at
            }
        
        except Exception as e:
            logger.error(f"Failed to get email details for {message_id}: {e}")
            return None
    
    def _parse_sender(self, sender):
        """Parse sender string to extract name and email"""
        try:
            if '<' in sender and '>' in sender:
                # Format: "Name <email@domain.com>"
                name_part = sender.split('<')[0].strip().strip('"')
                email_part = sender.split('<')[1].split('>')[0].strip()
                return name_part, email_part
            else:
                # Format: "email@domain.com" or just the email
                return sender, sender
        except:
            return sender, sender
    
    def _parse_date(self, date_str):
        """Parse email date string to datetime object"""
        try:
            # Remove timezone info for simplicity
            date_str = date_str.split('+')[0].split('-')[0].strip()
            return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S')
        except:
            return datetime.utcnow()
    
    def _extract_body(self, payload):
        """Extract email body from payload"""
        try:
            if 'parts' in payload:
                # Multipart message
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    elif part['mimeType'] == 'text/html':
                        if 'data' in part['body']:
                            # For HTML, we'll return a simplified version
                            html_content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            # Simple HTML to text conversion (basic)
                            import re
                            text_content = re.sub('<[^<]+?>', '', html_content)
                            return text_content.strip()
            else:
                # Simple message
                if 'data' in payload['body']:
                    return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            
            return ""
        except Exception as e:
            logger.error(f"Failed to extract body: {e}")
            return ""
