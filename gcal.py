from event import Event
import argparse
import utils
import reqs
import printer
from date import Date
from datetime import date
from sys import stderr

def main():
    reqs.init()
    utils.loadEmails()

    flags = parseArgs()
    calendars = utils.loadCalendars()

    if flags.calendar:
        try:
            calendarId = calendars[flags.calendar]
        except KeyError:
            print('Invalid calendar name:',flags.calendar, file=stderr)
            return 1

    if flags.new_event:
        newEvent(calendarId)

    elif flags.list:
        listEvents(calendarId)

    elif flags.agenda:
        showAgenda(calendarId)
    
    elif flags.quick:
        if len(flags.quick) < 2:
            print('Invalid format for a quick event', file=stderr)
            print('Usage: --quick DATE[TIME] , SUMMARY', file=stderr)
            return 1

        quickEvent(calendarId, ' '.join(flags.quick))

    else:
        # no main flag provided
        #TODO implement a menu
        print('not implemented')


def parseArgs():
    parser = argparse.ArgumentParser(prog='gcal',description='Google Calendar command line client')
    parser.add_argument('-n','--new-event', dest='new_event', action='store_true', help='create a new event')
    parser.add_argument('-c','--calendar', dest='calendar', action='store', default='main', help='select the calendar (default is primary calendar)')
    parser.add_argument('-l','--list', dest='list', action='store_true', help='list events for the selected calendar')
    parser.add_argument('-a','--agenda', dest='agenda', action='store_true', help='show agenda for the selected calendar')
    parser.add_argument('-q','--quick',dest='quick',action='store', nargs='*', help='create an event quickly')
    return parser.parse_args()


def newEvent(calendarId):
    event = Event.readEvent()

    # insert event into calendar
    reqs.insertEvent(event.toDict(),calendarId)

def quickEvent(calendarId: str, qe: str):
    
    date, summary = qe.split(',', maxsplit=1)
    date.strip()
    summary.strip()

    try:
        date = Date.fromUserInput(date)
    except Exception as e:
        print(e, file=stderr)
        return 1

    e = Event.quick(summary,date)
    reqs.insertEvent(e.toDict(), calendarId)

def listEvents(calendarId):
    events = reqs.listEvents(calendarId)
    for e in events:
        print(Event.parse(e))

def showAgenda(calendarId):
    events = reqs.agenda(calendarId)
    events = list(map(lambda x: Event.parse(x), events))

    today = date.today()
    # TODO dateNextWeekday(7) is invalid as weekdays range from 0 to 6
    # find out what's wrong in the method
    nextSunday = Date.dateNextWeekday(7)
    days = (nextSunday - today).days

    printer.printAgenda(events,today,days)

    #for e in events:
    #    print(Event.parse(e))

if __name__ == '__main__':
    main()