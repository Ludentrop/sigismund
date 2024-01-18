import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # depends on the scope you've specified in your google developer environment

SPREADSHEET_ID = 'spreadsheetId'


def auth():
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    return credentials


def get_data(credentials):
    try:
        service = build('sheets', 'v4', credentials=credentials)

        row = len(
            service
            .spreadsheets()
            .values()
            .get(spreadsheetId=SPREADSHEET_ID, range='answers!A1:G')  # in my google sheets the page name was "answer", and columns from A to G
            .execute()['values'])

        sheets = service.spreadsheets()

        result = sheets.values().get(
            spreadsheetId=SPREADSHEET_ID, range=f'answers!A{row}:G{row}').execute()['values'][0]

        return result

    except HttpError as error:
        print(error)
        return 0
