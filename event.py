import utils
from utils import Date
from datetime import datetime

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
            out += self.start.getDate() + ' * ' + self.start.getTime() + "-" + self.end.getTime()
        elif self.type == 'allday':
            out += self.start.getDate()
        else:   # multidate
            out += self.start.getDate() + ', ' + self.start.getTime() + "-" + self.end.getDate() + ', ' + self.end.getTime()
        
        if self.location:
            out += ' [' + self.location + ']\n'
        else:
            out += '\n'

        if self.extra:
            out += '[' + self.recurrence() + ']\n'
        
        return out

    def toDict(self):
        out = vars(self)
        # set key according to type of date: all day or not
        key = 'date' if self.start.hour == None else 'dateTime'
        out['start'] = {key: utils.Date.toRFC3339(self.start)}
        out['end'] = {key: utils.Date.toRFC3339(self.end)}
        # delete unnecessary properties
        del(out['type'])
        del(out['extra'])
        return out

    def recurrence(self):
        tokens = self.extra['recurrence']
        count = None
        interval = None
        until = None
        byday = None
        out = ''

        for t in tokens:
            k,v = t.split('=')
            if k =='RRULE:FREQ':
                freq = v
                if freq == 'DAILY':
                    freq = 'days'
                elif freq == 'WEEKLY':
                        freq = 'weeks'
                elif freq == 'MONTHLY':
                    freq = 'months'
                else:
                    freq = 'years'

            elif k == 'WKST':
                continue
            elif k == 'COUNT':
                count = v
            elif k == 'INTERVAL':
                interval = v
            elif k == 'UNTIL':
                until = v
                until = datetime.strptime(v,'%Y%m%dT%H%M%SZ').strftime('%d/%m/%Y')
            elif k == 'BYDAY':
                byday = v
        
        if not interval:
            interval = 1

        out += 'every {} {}'.format(interval,freq)

        if byday:
            out += ' on {}'.format(byday)

        if count:
            out += ' for {} times'.format(count)
        elif until:
            out += ' until {}'.format(until)

        return out

    @staticmethod
    def parse(e):
        key = 'date' if 'date' in e['start'] else 'dateTime'
        start = Date.fromRFC3339(e['start'][key])
        end = Date.fromRFC3339(e['end'][key])
        description = None if 'description' not in e else e['description']
        location = None if 'location' not in e else e['location']
        extra = None
        if 'recurrence' in e:
            extra = {'recurrence': e['recurrence'][0].split(';')}
        
        return Event(e['summary'],description,start,end,location,extra)

    @staticmethod
    def readEvent():
        correct = False
        name = input('Name: ')
        while not correct:
            start = input('Start: ')    # 15 03 2019[ 14 00]
            try:
                start = Date.fromUserInput(start)
            except:
                print('Invalid date format')
            else:
                correct = True

        correct = False
        while not correct:
            end = input('End: ')
            try:
                end = Date.fromUserInput(end)
            except:
                print('Invalid date format')
            else:
                correct = True
         
        location = input('Location: ')
        description = input('Description: ')

        return Event(name,description,start,end,location,None)