import datetime
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/calendar.events']
service = None
creds = None

def init():
    global service
    global creds
    creds = loadCreds()
    service = build('calendar', 'v3', credentials=creds)

def loadCreds():
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
    
    return creds
    

def insertEvent(event,calendarId):
    event = service.events().insert(calendarId=calendarId, body=event).execute()

def listEvents(calendarId, timeMin = 0, maxResults = 10):
    if timeMin == 0:
        timeMin = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events_result = service.events().list(calendarId=calendarId, timeMin=timeMin,
                                          maxResults=maxResults, singleEvents=False
                                          ).execute()
    return events_result.get('items', [])

def agenda(calendarId, timeMin = 0, maxResults = 10):
    if timeMin == 0:
        timeMin = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events_result = service.events().list(calendarId=calendarId, timeMin=timeMin,
                                          maxResults=maxResults, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])
    