import utils

class Event:
    '''The event object'''
    def __init__(self,summary,description, start, end, location, extra):
        self.summary = summary
        self.location = location
        self.description = description
        self.start = utils.toGDate(start)
        self.end = utils.toGDate(end)

        if extra:
            # unpack extra
            # attendees, recurrence, reminders
            print(extra)

    
    def __str__(self):
        return self.summary + '\n' + self.description + '\n' + self.location + '\n' + str(self.start) + '\n' + str(self.end)

    @staticmethod
    def parse(e):
        start = utils.toDate(e['start'])
        end = utils.toDate(e['end'])
        description = '' if 'description' not in e else e['description']
        location = '' if 'location' not in e else e['location']
        return Event(e['summary'],description,start,end,location,None)