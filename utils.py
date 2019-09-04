import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import date, timedelta, datetime
from reqs import SCOPES

creds = None

def loadCreds():
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

class Date:
    '''Utility date class'''
    def __init__(self,day,month,year,hour,minute,timezone):
        self.day = day
        self.month = month
        self.year = year
        self.hour = hour
        self.minute = minute
        self.timezone = timezone

    def toRFC3339(self):
        # output: "yyyy-mm-ddThh:mm:ss[+-]tz:tz"
        return '{}-{}-{}T{}:{}:00{}'.format(
            self.year, self.month, self.day, self.hour, self.minute, self.timezone
        )

    def __str__(self):
        out = '{}/{}/{}'.format(self.day, self.month, self.year)
        if self.hour:
            out += ' {}:{}'.format(self.hour,self.minute)
        return out

    
    #def __repr__(self):
    #    key = 'date' if self.start.hour == None else 'dateTime'
    #    return str({
    #        'dateTime': self.toRFC3339()
    #    })

    @staticmethod
    def fromRFC3339(s):
        # parses a date in the RFC3339's format "yyyy-mm-dd[Thh:mm:ss[+-tz:tz]]" to date object
        if 'T' in s:
            # s contains both date and time
            date, time = s.split('T')
            year,month,day = date.split('-')
            hour,minute = time.split(':')[:2]
            return Date(day,month,year,hour,minute,None)
        else:
            # s contains date only
            year,month,day = s.split('-')
            return Date(day,month,year,None,None,None)
        
        #timezone = 'UTC' if time[-1] == 'Z' or time.endswith('+00:00') else time[-6:]

    @staticmethod
    def fromStandard(s):
        # parses a date in the standard format "dd/mm/yyyy hh:mm" to a date object
        date,time = s.split(' ')
        day,month,year = date.split('/')
        hour,minute = time.split(':')
        return Date(day,month,year,hour,minute,None)

    @staticmethod
    def fromUserInput(s):
        # tries to parse the user input for a date
        # raises an exception if the format is not valid
        # or date is not valid
        s = s.strip()
        # check wildcards 'today' and 'tomorrow'
        if s.startswith('today'):
            year, month, day = date.today().timetuple()[:3]
            hour, minute = s.split(' ')[1:]
        elif s.startswith('tomorrow'):
            year, month, day = (date.today() + timedelta(days=1)).timetuple()[:3]
            hour, minute = s.split(' ')[1:]
        else:
            # no wildcards
            day,month,year,hour,minute = s.split(' ')

        # check if date is valid
        try:
            d = '{} {} {} {} {}'.format(day,month,year,hour,minute)
            datetime.strptime(d, '%d %m %Y %H %M')
        except ValueError:
            raise Exception('Date format is not valid')
        else:
            return Date(day,month,year,hour,minute,'+02:00')
        