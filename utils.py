import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from reqs import SCOPES

creds = None

def toGDate(d):
    # converts date the the RFC3339 format
    # input:  dd/mm/yyyy hh:mm
    # output: yyyy-mm-ddThh:mm:ss- ...
    # a timeZone field will also be added
    date,time = d.split(' ')
    day,month,year = date.split('/')
    hour,minute = time.split(':')
    return {
        'dateTime': year + '-' + month + '-' + day + 'T' + hour + ':' + minute + ':00+02:00', # +02:00 is the central europe time zone
    }

def toDate(gd):
    # converts date from RFC3339's format to local format
    # input:  yyyy-mm-ddThh:mm:ss[+-]tz:tz ...
    # output: dd/mm/yyyy hh:mm
    date, time = gd['dateTime'].split('T')
    year,month,day = date.split('-')
    hour,minute = time[:5].split(':')
    
    timezone = 'UTC' if time[-1] == 'Z' or time.endswith('+00:00') else time[-6:]
    return day + '/' + month + '/' + year + ' ' + hour + ':' + minute

def readCreds():
    global creds
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
