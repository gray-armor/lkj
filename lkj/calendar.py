from datetime import datetime
import os
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Calendar:
    def __init__(self, token_path: Path, credential_path: Path) -> None:
        self.token_path = token_path
        self.credential_path = credential_path
        self.creds = None

    def authorize(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if self.is_authorized():
            return

        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(self.credential_path, SCOPES)
            self.creds = flow.run_local_server(port=0)
        with open(self.token_path, 'w') as token:
            token.write(self.creds.to_json())

    def is_authorized(self) -> bool:
        return self.creds and self.creds.valid

    def print_items(self):
        if self.is_authorized:
            self.authorize()

        service = build('calendar', 'v3', credentials=self.creds)
        now = datetime.utcnow().isoformat() + 'Z'
        print("Getting the upcoming 10 events")
        event_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = event_result.get('item', [])
        if not events:
            print('No upcoming events found')

        for event in events:
            start = event['start'].get("dateTime", event['start'].get('date'))
            print(start, event['summary'])
