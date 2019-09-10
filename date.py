from datetime import datetime, date, timedelta, tzinfo

class TZ(tzinfo):
    def utcoffset(self, dt): return timedelta(minutes=+120)
    
    @staticmethod
    def tzname(): return 'Europe/Rome'

    def dst(self,dt): return timedelta(0)

class Date(datetime):
    '''Utility Date class'''
    pass

    weekdays = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

    def __str__(self) -> str:
        if self.hasTime:
            return self.strftime('%d/%m/%Y %H:%M')
        else:
            return self.strftime('%d/%m/%Y')

    def dateEquals(self,d) -> bool:
        return self.date() == d.date()

    def dateStr(self) -> str:
        return self.date().strftime('%d/%m/%Y')

    def timeStr(self) -> str:
        return self.time().strftime('%H:%M')

    @staticmethod
    def new(year,month,day,hour,minute,hasTime):
        out = Date(year,month,day,hour,minute,tzinfo=TZ())
        out.hasTime = hasTime
        return out

    @staticmethod
    def fromDatetime(dt, hasTime):
        return Date.new(dt.year, dt.month, dt.day, dt.hour, dt.minute,hasTime)

    @staticmethod
    def weekDayNumber(day):
        day = day.capitalize()
        for k,v in Date.weekdays.items():
            if v == day:
                return k

        return None

    @staticmethod
    def dateNextWeekday(dayNumber):
        # Returns the date corresponding to the next weekday from today

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
    def fromUserInput(s: str):
        # Tries to parse a date object from a user input for a date
        # possible inputs: today 11 30 - tomorrow 11 30 - 31 12 2019 11 30
        
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
            dayNumber = Date.weekDayNumber(day)
            if dayNumber is None:
                raise Exception('Invalid week day: ' + day)
                
            nextDate = Date.dateNextWeekday(dayNumber)
            year, month, day = nextDate.timetuple()[:3]

        elif not dateTokens[0].isdigit():
            # first token is neither a number nor a valid wildcard
            raise Exception('Invalid token: ' + dateTokens[0])

        else:
            # no wildcards
            if len(dateTokens) < 3:
                raise Exception('Not enough tokens for a date')

            day,month,year = dateTokens[:3]

        if len(dateTokens) > timeStartIndex:
            hour,minute = dateTokens[timeStartIndex:]
            hasTime = True

        try:
            return Date.new(int(year), int(month), int(day), int(hour), int(minute), hasTime)
        except ValueError:
            raise Exception('Invalid date')