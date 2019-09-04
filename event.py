import utils
from utils import Date


class Event:
    '''The event object'''
    def __init__(self,summary,description, start, end, location, extra):
        self.summary = summary
        self.location = location
        self.description = description
        self.start = start
        self.end = end

        if extra:
            # unpack extra
            # attendees, recurrence, reminders
            print(extra)

    
    def __str__(self):
        return 'Summary: {} \nDescription: {} \nLocation: {} \nFrom: {} to {}'.format(self.summary, self.description, self.location, str(self.start), str(self.end))

    def toDict(self):
        out = vars(self)
        # set key according to type of date: all day or not
        key = 'date' if self.start.hour == None else 'dateTime'
        out['start'] = {key: utils.Date.toRFC3339(self.start)}
        out['end'] = {key: utils.Date.toRFC3339(self.end)}
        print(out)
        return out

    @staticmethod
    def parse(e):
        key = 'date' if 'date' in e['start'] else 'dateTime'
        start = Date.fromRFC3339(e['start'][key])
        end = Date.fromRFC3339(e['end'][key])
        description = '' if 'description' not in e else e['description']
        location = '' if 'location' not in e else e['location']
        return Event(e['summary'],description,start,end,location,None)

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