import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from django.contrib.staticfiles import finders
from django.conf import settings
import os



SCOPES = ["https://www.googleapis.com/auth/calendar", ]

def getCalendarService():
    creds = None
    token_path = os.path.join(settings.BASE_DIR, 'calendar_challange', 'tokens.json')
    credentials_secret = os.path.join(settings.BASE_DIR, 'calendar_challange', 'credentials.json')
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_secret, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as tokens:
            tokens.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service
        