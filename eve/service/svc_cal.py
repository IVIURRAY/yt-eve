import datetime
import os

import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from eve.config import PATH_TO_CALENDAR_API_CRED, DEFAULT_CALENDAR_EVENTS_NUMBER
from ..utilities import utils as f


def build_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../../token.json'):
        creds = Credentials.from_authorized_user_file('../../token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                # path should contain file itself, e.g '/Users/john/cred/credentials.json
                PATH_TO_CALENDAR_API_CRED, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../../token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


class Calendar:

    def __init__(self):
        self.service = build_service()

    def next(self):
        now = datetime.datetime.now(tz=pytz.UTC).isoformat()  # Google calendar api expects date in UTC
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=DEFAULT_CALENDAR_EVENTS_NUMBER, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = []
        for e in events_result.get('items', []):
            starts_in = f.get_time_diff(str(e["start"]["dateTime"]), str(datetime.datetime.now(tz=pytz.UTC)))
            events.append({"name": e["summary"],
                           "organizer": e["organizer"]["email"],
                           "status": e["status"].capitalize(),
                           "starts_in": f'{starts_in.seconds // 60 if starts_in.days >= 0 else "In Progress"}',
                           "duration": str(f.get_time_diff(str(e["end"]["dateTime"]),
                                                           str(e["start"]["dateTime"])).seconds // 60) + " min"
                           })
        return events
