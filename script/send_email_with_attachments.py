"""Send an email message from the user's account.
"""

import os
import json
import base64
import pickle
import os.path
import mimetypes

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']


def service_authentication():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
                                filename):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  main_type, sub_type = content_type.split('/', 1)
  fp = open(path, 'rb')
  msg = MIMEBase(main_type, sub_type)
  msg.set_payload(fp.read())

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  encoders.encode_base64(msg)

  fp.close()

  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(bytes(message.as_string(), encoding='utf-8')).decode()}

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """

  message_resp = (service.users().messages().send(userId=user_id, body=message).execute())
  print("Sucessfull!!! ", message_resp)

def main():
    sender = 'souzaharison2@gmail.com'
    to = 'souzaharison2@99app.com'
    subject = 'Harison'
    message_text = 'Olá Harison, tudo bem???'
    file_dir = '/Users/harison.souza/Documents/teste'
    filename = 'send_to_gmail.csv'

    service = service_authentication()
    message = CreateMessageWithAttachment(sender=sender, to=to, subject=subject, message_text=message_text, file_dir=file_dir, filename=filename)
    SendMessage(service=service, user_id='me', message=message)

if __name__ == "__main__":
    main()