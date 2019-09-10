import utils
import rrule
from date import Date, TZ
from datetime import datetime, timedelta

class Event:
    '''The event object'''
    def __init__(self,summary,description, start, end, location, recurrence, attendees):
        self.summary = summary
        self.location = location
        self.description = description
        self.start = start
        self.end = end
        self.recurrence = recurrence
        self.attendees = attendees
        
        # event type
        if not self.start.hasTime:
            self.type = 'allday'
        elif self.start.dateEquals(self.end):
            self.type = 'singleday'
        else:
            self.type = 'multiday'

    
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

        if self.recurrence:
            out += '[' + rrule.toStr(self.recurrence) + ']'

        if self.attendees:
            out += '[with {}]'.format(', '.join(self.attendees))
        
        return out

    def toDict(self):
        out = vars(self)
        # set key according to type of date: all day or not
        key = 'dateTime' if self.start.hasTime else 'date'

        startValue = self.start.isoformat()
        endValue = self.end.isoformat()

        if key == 'date':
            # remove time from iso formatted values
            startValue = startValue.split('T')[0]
            endValue = endValue.split('T')[0]

        out['start'] = {key: startValue}
        out['end'] = {key: endValue}

        # add timeZone to start,end if they contains time
        if key == 'dateTime':
            tz = {'timeZone': TZ.tzname()}
            out['start'].update(tz)
            out['end'].update(tz)

        # delete unnecessary properties
        del(out['type'])
        if out['attendees']:
            out['attendees'] = list(map(lambda x: {'email': x}, out['attendees']))
        else:
            del out['attendees']

        if out['recurrence']:
            # represent recurrence as an array
            out['recurrence'] = [ out['recurrence'] ]
        else:
            del out['recurrence']
        
        return out

    @staticmethod
    def parse(e):
        hasTime = 'dateTime' in e['start']
        key = 'dateTime' if hasTime else 'date'
        start = Date.fromDatetime(datetime.fromisoformat(e['start'][key]), hasTime)
        end = Date.fromDatetime(datetime.fromisoformat(e['end'][key]), hasTime)
        description = None if 'description' not in e else e['description']
        location = None if 'location' not in e else e['location']
        
        recurrence = e['recurrence'][0] if 'recurrence' in e else None
        attendees = list(map(lambda x: x['email'], e['attendees'])) if 'attendees' in e else None
 
        return Event(e['summary'],description,start,end,location,recurrence, attendees)

    @staticmethod
    def quick(summary,dateStart):
        # creates an event with only a summary and a duration of 1 hour
        dateEnd = Date.fromDatetime(dateStart + timedelta(hours=1), hasTime=True)
        return Event(summary,None,dateStart,dateEnd,None,None,None)

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

        description, recurrence, attendees = None, None, None
        if input('Extra fields? (y/n): ')  == 'y':
            
            description = input('Description: ')

            correct = False
            while not correct:
                try:
                    recurrence = input('recurrence: ')
                    if recurrence == '':
                        recurrence = None
                    else:
                        recurrence = rrule.fromUserInput(recurrence)
                except Exception as e:
                    print(e)
                else:
                    correct =  True
                    
            correct = False
            while not correct:
                try:
                    attendees = input('with: ')
                    if attendees == '':
                        attendees = None
                    else:
                        attendees = utils.parseAttendees(attendees)

                except KeyError as e:
                    print('Invalid name: ' + str(e))
                else:
                    correct = True
        
        return Event(name,description,start,end,location,recurrence, attendees)