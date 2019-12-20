import datetime
import os.path
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar.readonly']
service = None

def init():
    global service
    creds = loadCreds()
    service = build('calendar', 'v3', credentials=creds)

def loadCreds():
    '''Loads the user's credentials (if existing), otherwise
    prompts the user to allow this program to access his google account, and
    generates new credentials.'''
    
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
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
    return creds
    

def insertEvent(event,calendarId):
    service.events().insert(calendarId=calendarId, body=event).execute()

def listEvents(calendarId, timeMin = 0, maxResults = 100):
    if timeMin == 0:
        timeMin = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events_result = service.events().list(calendarId=calendarId, timeMin=timeMin,
                                          maxResults=maxResults, singleEvents=False
                                          ).execute()
    return events_result.get('items', [])

def agenda(calendarId, timeMin, timeMax, maxResults = 100):
    page_token = None
    # TODO implement pagination based on page_token
    events_result = service.events().list(calendarId=calendarId, timeMin=timeMin,
                                          timeMax=timeMax, maxResults=maxResults,
                                          singleEvents=True, orderBy='startTime').execute()

    return events_result.get('items', [])

def getCalendars():
    '''Requests all the calendars and saves their names and ids in `calendars.json`'''
    calendars = {}
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for entry in calendar_list['items']:
            name, id = entry['summary'], entry['id']
            if name == id:
                name, id = 'main', 'primary'

            calendars[name] = id

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    _saveCalendars(calendars)

def _saveCalendars(calendars):
    '''Writes *calendars* entries to the file `calendars.json`'''
    with open('calendars.json','w', encoding='utf-8') as f:
        f.write(json.dumps(calendars, indent=4, ensure_ascii=False))
