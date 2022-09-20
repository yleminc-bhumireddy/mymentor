import cachecontrol
import flask
import base64
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import html2text
import google.auth
import googleapiclient
from google.auth.transport import requests
from google.oauth2 import id_token
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def gmail_send(emailForm):
    """Create and insert a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """
    # creds, _ = google.auth.default()
    creds = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    primary_alias = get_current_user_id(creds)
    total_messages = 0

    service = build('gmail', 'v1', credentials=creds)
    for to in emailForm.tolist.data.split(','):
        try:
            message = EmailMessage()
            plain_text = emailForm.emailBody.data + '\n\n' + primary_alias.get('signature')
            # message.set_content(emailForm.emailBody.data)

            message['To'] = to
            message['From'] = 'Venkata Bhumireddy'
            message['Subject'] = emailForm.subject.data
            message.add_header('Content-Type', 'text/html')
            message.add_alternative(plain_text, subtype='html')

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                .decode()

            create_message = {
                'raw': encoded_message
            }
            send_as_configuration = {
                'displayName': primary_alias.get('displayName'),
                'signature': 'Automated Signature'
            }

            # pylint: disable=E1101
            send_message = (service.users().messages().send
                            (userId="me",  body=create_message, ).execute())
            print(F'Message Id: {send_message["id"]}')
            total_messages = total_messages + 1
        except HttpError as error:
            print(F'An error occurred: {error}')
    return total_messages


def get_current_user_id(creds):
    primary_alias = None
    # token_request = google.auth.transport.requests.Request(session=flask.session)
    service = build('gmail', 'v1', credentials=creds)
    aliases = service.users().settings().sendAs().list(userId='me').execute()
    for alias in aliases.get('sendAs'):
        print(str(alias))
        if alias.get('isPrimary'):
            primary_alias = alias
            break
    print(primary_alias)
    return primary_alias
