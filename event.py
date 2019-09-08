import utils
import rrule
from date import Date
from datetime import datetime, timedelta

class Event:
    '''The event object'''
    def __init__(self,summary,description, start, end, location, extra):
        self.summary = summary
        self.location = location
        self.description = description
        self.start = start
        self.end = end
        self.extra = extra
        
        # event type
        if not self.start.hasTime:
            self.type = 'allday'
        elif self.start.dateEquals(self.end):
            self.type = 'singleday'
        else:
            self.type = 'multiday'

        if extra:
            # unpack extra
            # attendees, recurrence, reminders
            'not implemented'

    
    def __str__(self):
        out = self.summary + ' '

        if self.description:
            out += '[' + self.description + ']\n'

        if self.type == 'singleday':
            out += self.start.dateStr() + ' * ' + self.start.timeStr() + "-" + self.end.timeStr()
        elif self.type == 'allday':
            out += self.start.dateStr()
        else:   # multidate
            out += str(self.start) + " - " + str(self.end)
        
        if self.location:
            out += ' [' + self.location + ']\n'
        else:
            out += '\n'

        if self.extra:
            #TODO self.extra['recurrence'] has to be a string not a list
            out += '[' + rrule.toStr(self.extra['recurrence']) + ']\n'
        
        return out

    def toDict(self):
        out = vars(self)
        # set key according to type of date: all day or not
        key = 'dateTime' if self.start.hasTime else 'date'
        out['start'] = {key: self.start.isoformat()}
        out['end'] = {key: self.end.isoformat()}

        # delete unnecessary properties
        del(out['type'])
        del(out['extra'])
        return out

    @staticmethod
    def parse(e):
        hasTime = 'dateTime' in e['start']
        key = 'dateTime' if hasTime else 'date'
        start = Date.fromDatetime(datetime.fromisoformat(e['start'][key]), hasTime)
        end = Date.fromDatetime(datetime.fromisoformat(e['end'][key]), hasTime)
        description = None if 'description' not in e else e['description']
        location = None if 'location' not in e else e['location']
        extra = None
        if 'recurrence' in e:
            extra = {'recurrence': e['recurrence'][0]}
        
        return Event(e['summary'],description,start,end,location,extra)

    @staticmethod
    def quick(summary,dateStart):
        # creates an event with only a summary and a duration of 1 hour
        dateEnd = Date.fromDatetime(dateStart + timedelta(hours=1), hasTime=True)
        return Event(summary,None,dateStart,dateEnd,None,None)

    @staticmethod
    def readEvent():
        correct = False
        name = input('Name: ')
        while not correct:
            start = input('Start: ')    # 15 03 2019[ 14 00]
            try:
                start = Date.fromUserInput(start)
            except Exception as e:
                print(e)
            else:
                correct = True

        correct = False
        while not correct:
            end = input('End: ')
            try:
                end = Date.fromUserInput(end)
            except Exception as e:
                print(e)
            else:
                correct = True
         
        location = input('Location: ')
        description = input('Description: ')
        input('Extra (y,n): ')
        if _ == 'y':
            recurrence = input('recurrence: every ')
            correct = False
            while not correct:
                try:
                    recurrence = rrule.fromUserInput(recurrence)
                except Exception as e:
                    print(e)
                else:
                    correct =  True
                    

        return Event(name,description,start,end,location,None)