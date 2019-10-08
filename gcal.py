#!/usr/bin/env python3

from event import Event
import argparse
import utils
import reqs
import printer
from date import Date
from datetime import date, timedelta
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
        showAgenda(calendarId, flags.agenda)
    
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
    parser.add_argument('-a','--agenda', dest='agenda', action='store', const='week', nargs='?',
                        choices=['day','3days','week','nextweek'], help='show agenda for the selected calendar')
    parser.add_argument('-q','--quick',dest='quick',action='store', nargs='*', help='create an event quickly')
    return parser.parse_args()


def newEvent(calendarId):
    '''Reads an event and adds it to the calendar
    identified by *calendarId*'''

    event = Event.readEvent()

    # insert event into calendar
    reqs.insertEvent(event.toDict(),calendarId)

def quickEvent(calendarId: str, qe: str):
    '''Tries to parse the input text for a quick event *qe*,
    and adds it to the calendar identified by *calendarId*'''
    
    date, summary = qe.split(',', maxsplit=1)
    date.strip()
    summary.strip()

    try:
        date = Date.fromUserInput(date)
    except ValueError as ve:
        print(ve, file=stderr)
        return 1

    e = Event.quick(summary,date)
    reqs.insertEvent(e.toDict(), calendarId)

def listEvents(calendarId):
    '''Lists the incoming events for the calendar identified by *calendarId*'''

    events = reqs.listEvents(calendarId)
    for e in events:
        print(Event.parse(e))

def showAgenda(calendarId, period):
    '''Prints the agenda for the calendar identified by *calendarId*,
    for the specified *period* in `['day','3days','week','nextweek']`.
    '''

    today = date.today()
    dateStart = today

    if period == 'day':
        days = 0
    elif period == '3days':
        days = 2
    elif period == 'week':
        nextSunday = Date.dateNextWeekday(6)
        days = (nextSunday - today).days   
    elif period == 'nextweek':
        dateStart = Date.dateNextWeekday(0)
        days = 6

    # request the events according to starting and ending dates.
    timeMin = dateStart.isoformat() + 'T00:00:00Z'
    timeMax = (dateStart + timedelta(days=days)).isoformat() + 'T23:59:59Z'

    events = reqs.agenda(calendarId, timeMin, timeMax)
    events = list(map(lambda x: Event.parse(x), events))

    printer.printAgenda(events,dateStart,days)

if __name__ == '__main__':
    main()
