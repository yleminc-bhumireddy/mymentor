from __future__ import print_function

import os.path

import google_auth_httplib2
import httplib2
import flask
import google.oauth2.credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
# from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.modules.login.routes import authorize
# from Google import Create_Service

# from app.modules.login.routes import flow

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


def readSheets():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # authorize()
    credentials = google.oauth2.credentials.Credentials(
                **flask.session['credentials'])
    credentials.refresh_token
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('token.json'):
    #     print("I am in if")
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     print("no creds")
    #     if creds and creds.expired and creds.refresh_token:
    #         print("token if")
    #         creds.refresh(Request())
    #     else:
    #         print("token else")
    # flow = InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file=os.path.join(os.getcwd(), 'env/client_secret.json'),
    #     scopes=SCOPES)
    # #         print("Flow created")
    # #         creds = flow.credentials
    # print("creds created")
    # refresh_http = httplib2.Http()
    # request = google_auth_httplib2.Request(refresh_http)
    # creds.refresh(flow.credentials)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=credentials)
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
        # # Call the Sheets API
        # sheet = service.spreadsheets()
        # result = sheet.values().get().execute()
        # values = result.get('values', [])
        #
        # if not values:
        #     print('No data found.')
        #     return
        #
        # print('Name, Major:')
        # for row in values:
        #     # Print columns A and E, which correspond to indices 0 and 4.
        #     print('%s, %s' % (row[0], row[4]))
    except HttpError as err:
        print(err)

def get_credentials_from_http(http):
    if http is None:
        return None
    elif hasattr(http.request, "credentials"):
        return http.request.credentials
    elif hasattr(http, "credentials") and not isinstance(
        http.credentials, httplib2.Credentials
    ):
        return http.credentials
    else:
        return None


def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = flask.session[AUTH_TOKEN_KEY]

    return google.oauth2.credentials.Credentials(
        oauth2_tokens['access_token'],
        refresh_token=oauth2_tokens['refresh_token'],
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri=ACCESS_TOKEN_URI)