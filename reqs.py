import datetime
import utils
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CALENDAR_IDS = ''
service = None

def init():
    global service
    service = build('calendar', 'v3', credentials=utils.creds)
    

def insertEvent(event,calendarId):
    event = service.events().insert(calendarId=calendarId, body=event.toDict()).execute()

def listEvents(timeMin = 0, maxResults = 10):
    if timeMin == 0:
        timeMin = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events_result = service.events().list(calendarId='primary', timeMin=timeMin,
                                          maxResults=maxResults, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])
