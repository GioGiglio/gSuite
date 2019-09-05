from event import Event
import argparse
import utils
import reqs

def main():
    reqs.init()

    flags = parseArgs()
    calendars = utils.loadCalendars()
    calendar = None

    if flags.calendar:
        calendar = calendars[flags.calendar]

    if flags.new_event:
        newEvent(calendars, calendar)

    elif flags.list:
        listEvents(calendar)


def parseArgs():
    parser = argparse.ArgumentParser(prog='gcal',
        description='Google Calendar CL client')
    parser.add_argument('-n','--new-event', dest='new_event', action='store_true')
    parser.add_argument('-c','--calendar', dest='calendar', action='store')
    parser.add_argument('-l','--list', dest='list', action='store_true')
    #print(parser.parse_args(['-c','primary']))

    return parser.parse_args()


def newEvent(calendars, calendarId):
    event = Event.readEvent()

    if not calendarId:
        calendarId = readCalendarId(calendars)
    
    # insert event into calendar
    reqs.insertEvent(event.toDict(),calendarId)

def listEvents(calendarId):

    if not calendarId:
        calendarId = 'primary'

    events = reqs.listEvents(calendarId)
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