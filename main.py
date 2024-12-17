### AUTHENTICATION WITH GMAIL

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

### CREATE A BULK SENDER SCRIPT

from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent: {message['id']}")
    except Exception as error:
        print(f"An error occurred: {error}")

def send_bulk_emails(creds, sender, recipients, subject, body):
    service = build('gmail', 'v1', credentials=creds)
    for recipient in recipients:
        msg = create_message(sender, recipient, subject, body)
        send_message(service, 'me', msg)

# Authenticate and send bulk emails
if __name__ == '__main__':
    creds = authenticate_gmail()
    sender_email = "sender@gmail.com"
    recipients_list = ["user1@gmail.com", "user2@gmail.com", "user3@gmail.com"]  # Add more as needed
    subject = "Automated Bulk Email"
    body = "This is a test email sent using Python and Gmail API."
    send_bulk_emails(creds, sender_email, recipients_list, subject, body)