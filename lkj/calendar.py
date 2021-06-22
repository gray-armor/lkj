from datetime import datetime, timezone
import os
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar.readonly'
]

class Calender:
    def __init__(self, id: str, summary: str):
        self.id = id
        self.summary = summary

class CalendarService:
    def __init__(self, token_path: Path, credential_path: Path) -> None:
        self.token_path = token_path
        self.credential_path = credential_path
        self.creds = None

    def __authorize(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if self.__is_authorized():
            return

        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        else:
            print("=========== Google Calendar Authentication ===========")
            flow = InstalledAppFlow.from_client_secrets_file(self.credential_path, SCOPES)
            self.creds = flow.run_local_server(port=0, success_message="Thanks! You can close this tab. LKJ")
            print("======= Google Calendar Authentication Finished =======")
        with open(self.token_path, 'w') as token:
            token.write(self.creds.to_json())

    def __is_authorized(self) -> bool:
        return self.creds and self.creds.valid

    def __get_service(self):
        if not self.__is_authorized():
            self.__authorize()

        return build('calendar', 'v3', credentials=self.creds)

    def get_calendars(self):
        service = self.__get_service()
        try:
            result_items = service.calendarList().list().execute()["items"]
            if not isinstance(result_items, list):
                return None

            cal_list = [Calender(item["id"], item.get("summaryOverride") or item["summary"]) for item in result_items]
        except KeyError:
            return None

        return cal_list

    def to_utc(self, dt: datetime):
        t = dt.timestamp()
        return datetime.fromtimestamp(t, timezone.utc)

    def set_event(self, id: str, start: datetime, end: datetime, title: str,  message: str):
        service = self.__get_service()
        request = service.events().insert(
            calendarId=id,
            body={
                "summary": title,
                "description": message,
                "start": {
                    "dateTime": self.to_utc(start).isoformat(),
                    "timeZone": "Asia/Tokyo"
                },
                "end": {
                    "dateTime": self.to_utc(end).isoformat(),
                    "timeZone": "Asia/Tokyo"
                },
            },
        )
        try:
            request.execute()
        except Exception as e:
            print(e)
