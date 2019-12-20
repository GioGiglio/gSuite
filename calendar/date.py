from datetime import datetime, date, timedelta, tzinfo
from sys import stderr

class TZ(tzinfo):
    '''Class for time zone info objects'''
    def utcoffset(self, dt): return timedelta(minutes=+120)
    
    @staticmethod
    def tzname(): return 'Europe/Rome'

    def dst(self,dt): return timedelta(0)

class Date(datetime):
    '''Utility Date class'''
    pass

    weekdays = dict(Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6)

    def __str__(self):
        if self.hasTime:
            return self.strftime('%d/%m/%Y %H:%M')
        else:
            return self.strftime('%d/%m/%Y')

    def __add__(self,other):
        result = super().__add__(other)
        return Date.fromDatetime(result,self.hasTime)


    def dateEquals(self,other):
        '''Checks if the date is equal to the *other* date.'''
        try:
            # other may be a datetime/Date instance
            return self.date() == other.date()
        except AttributeError:
            # other is a datetime.date instance
            return self.date() == other

    def dateStr(self):
        '''Returns a string representation of the date
        according to the format `dd/mm/YYYY`.
        '''
        return self.strftime('%d/%m/%Y')

    def timeStr(self):
        '''Returns a string representation of the time
        according to the format `HH:MM`.'''
        return self.strftime('%H:%M')

    @staticmethod
    def new(year,month,day,hour,minute,hasTime):
        '''Returns a new *Date* object.'''
        out = Date(year,month,day,hour,minute,tzinfo=TZ())
        out.hasTime = hasTime
        return out

    @staticmethod
    def fromDatetime(dt, hasTime):
        '''Returns a new *Date* object created from the *dt* datetime object'''
        return Date.new(dt.year, dt.month, dt.day, dt.hour, dt.minute,hasTime)

    @staticmethod
    def dateNextWeekday(dayNumber):
        '''Returns the *Date* corresponding to the next weekday occurrence starting from the current day.
        *dayNumber* identifies the weekday as an integer where Monday is 0 and Sunday is 6.'''

        if not 0 <= dayNumber <= 6:
            raise ValueError('Invalid day number: ' + str(dayNumber))

        today = date.today()
        currentDayNumber = today.weekday()

        if dayNumber <= currentDayNumber:
            days = 7 - currentDayNumber
            days += dayNumber % 7
        else:
            days = dayNumber - currentDayNumber
        
        nextDate = today + timedelta(days=days)
        return nextDate

    @staticmethod
    def fromUserInput(s):
        '''Tries to parse a *Date* object from a text input for a date.
        
        Read *How a Date is defined* for further information on date representations.'''
        
        s = s.strip()
        dateTokens = s.split(' ')
        hasTime = False
        hour,minute = 0,0
        timeStartIndex = 3
        
        # replace wildcards with dates
        if s.startswith('today'):
            year, month, day = date.today().timetuple()[:3]
            timeStartIndex = 1
            
        elif s.startswith('tomorrow'):
            year, month, day = (date.today() + timedelta(days=1)).timetuple()[:3]
            timeStartIndex = 1

        elif s.startswith('next'):
            timeStartIndex = 2
            day = dateTokens[1]
            try:
                dayNumber = Date.weekdays[day.capitalize()]
                nextDate = Date.dateNextWeekday(dayNumber)
                year, month, day = nextDate.timetuple()[:3]
            except KeyError:
                raise ValueError('Invalid week day: ' + day)
            except ValueError as ve:
                print(ve, file=stderr)

        elif not dateTokens[0].isdigit():
            # first token is neither a number nor a valid wildcard
            raise ValueError('Invalid date token: ' + dateTokens[0])

        else:
            # no wildcards
            if len(dateTokens) < 3:
                raise ValueError('Not enough tokens for a date')

            day,month,year = dateTokens[:3]

        if len(dateTokens) > timeStartIndex:
            hour,minute = dateTokens[timeStartIndex:]
            hasTime = True

        try:
            return Date.new(int(year), int(month), int(day), int(hour), int(minute), hasTime)
        except ValueError:
            raise ValueError('Invalid date')