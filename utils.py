from datetime import date, timedelta, datetime
from reqs import SCOPES
import json

def loadCalendars():
    # read calendars
    with open('calendars.json','r') as f:
        calendars = json.load(f)
    return calendars

class Date:
    '''Utility date class'''
    def __init__(self,day,month,year,hour,minute,timezone):
        self.day = day
        self.month = month
        self.year = year
        self.hour = hour
        self.minute = minute
        self.timezone = timezone
        self.hasTime = hour != None

    def toRFC3339(self):
        # output: "yyyy-mm-dd[Thh:mm:ss+-tz:tz]"
        out =  '{}-{}-{}'.format( self.year, self.month, self.day)

        if self.hasTime:
            out += 'T{}:{}:00{}'.format(self.hour, self.minute, self.timezone)
        return out

    def __str__(self):
        out = '{}/{}/{}'.format(self.day, self.month, self.year)
        if self.hasTime:
            out += ' {}:{}'.format(self.hour,self.minute)
        return out

    def getDate(self):
        return '{}/{}/{}'.format(self.day, self.month, self.year)

    def getTime(self):
        return '{}:{}'.format(self.hour,self.minute) if self.hasTime else None

    def dateEquals(self,d):
        return self.day == d.day and self.month == d.month and self.year == d.year

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
            # check if s contains also time
            if ' ' in s:
                hour, minute = s.split(' ')[1:]
        elif s.startswith('tomorrow'):
            year, month, day = (date.today() + timedelta(days=1)).timetuple()[:3]
            # check if s contains also time
            if ' ' in s:
                hour, minute = s.split(' ')[1:]
        else:
            # no wildcards
            d = s.split(' ')
            day,month,year = d[:3]
            if len(d) > 3:
                hour,minute = d[3:5]

        # check if date is valid
        try:
            # validate date
            d = '{} {} {}'.format(day,month,year)
            datetime.strptime(d, '%d %m %Y')
            # validate time, if it exists
            if 'hour' in locals():
                d = '{} {}'.format(hour,minute)
                datetime.strptime(d,'%H %M')
                return Date(day,month,year,hour,minute,'+02:00')
            else:
                return Date(day,month,year,None,None,None)

        except ValueError:
            raise Exception('Date format is not valid')
        