from event import Event
import argparse
import utils
import reqs
from date import Date

def main():
    reqs.init()
    utils.loadEmails()

    flags = parseArgs()
    calendars = utils.loadCalendars()
    calendar = None

    if flags.calendar:
        calendar = calendars[flags.calendar]

    if flags.new_event:
        newEvent(calendars, calendar)

    elif flags.list:
        listEvents(calendar)

    elif flags.agenda:
        showAgenda(calendar)
    
    elif flags.quick:
        quickEvent(calendar, flags.quick)

    else:
        # no main flag provided
        #TODO implement a menu
        print('not implemented')


def parseArgs():
    parser = argparse.ArgumentParser(prog='gcal',
        description='Google Calendar CL client')
    parser.add_argument('-n','--new-event', dest='new_event', action='store_true', help='create a new event')
    parser.add_argument('-c','--calendar', dest='calendar', action='store', help='select the calendar (default is primary calendar)')
    parser.add_argument('-l','--list', dest='list', action='store_true', help='list events for the selected calendar')
    parser.add_argument('-a','--agenda', dest='agenda', action='store_true', help='show agenda for the selected calendar')
    parser.add_argument('-q','--quick',dest='quick',action='store', nargs='*', help='create an event quickly')
    return parser.parse_args()


def newEvent(calendars, calendarId):
    event = Event.readEvent()

    if not calendarId:
        calendarId = readCalendarId(calendars)
    
    # insert event into calendar
    reqs.insertEvent(event.toDict(),calendarId)

def quickEvent(calendarId, tokens):
    # format date time event_summary
    if not calendarId:
        calendarId = 'primary'

    if len(tokens) < 2:
        raise Exception('invalid format')

    s = ' '.join(tokens)
    
    date, summary = s.split(',', maxsplit=1)
    date.strip()
    summary.strip()
    date = Date.fromUserInput(date)

    e = Event.quick(summary,date)
    reqs.insertEvent(e.toDict(), calendarId)

def listEvents(calendarId):

    if not calendarId:
        calendarId = 'primary'

    events = reqs.listEvents(calendarId)
    for e in events:
        print(Event.parse(e))

def showAgenda(calendarId):
    if not calendarId:
        calendarId = 'primary'

    events = reqs.agenda(calendarId)

    for e in events:
        print(Event.parse(e))

def readCalendarId(calendars):
    print('Calendar (', end='')
    print(*calendars.keys(), sep=', ', end='')
    print('): ', end='')
    c = input()
    return calendars[c]


if __name__ == '__main__':
    main()