import utils


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
        return 'Summary: {} \nDescription: {} \nLocation: {} \nFrom: {} to {}'.format(self.summary, self.description, self.location, utils.toDate(self.start), utils.toDate(self.end))

    @staticmethod
    def parse(e):
        start = utils.toDate(e['start'])
        end = utils.toDate(e['end'])
        description = '' if 'description' not in e else e['description']
        location = '' if 'location' not in e else e['location']
        return Event(e['summary'],description,start,end,location,None)

    @staticmethod
    def readEvent():
        name = input('Name: ')
        start = input('Start: ')    # 15 03 2019 14 00
        #TODO check start date format

        # check date wildcards 'today' and 'tomorrow'
        if start.startswith('today'):
            start = start.replace('today',utils.todayDate())
        elif start.startswith('tomorrow'):
            start = start.replace('tomorrow',utils.tomorrowDate())
        
        start = utils.toGDate(utils.joinDate(start))
        
        end = input('End: ')
        # check date wildcards 'today' and 'tomorrow'
        if end.startswith('today'):
            end = end.replace('today',utils.todayDate())
        elif end.startswith('tomorrow'):
            end = end.replace('tomorrow',utils.tomorrowDate())

        end = utils.toGDate(utils.joinDate(end))
        
        location = input('Location: ')
        description = input('Description: ')

        return Event(name,description,start,end,location,None)