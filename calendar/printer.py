from copy import copy
from event import Event
from datetime import timedelta, date


def printAgenda(events, startDate, days):
    for i in range(days+1):
        d = startDate + timedelta(days=i)
        
        # startingEvents are the events having starting date equal to d
        startingEvents = list(filter(lambda x: x.start.dateEquals(d), events))

        # occurringEvents are the events that last more than one day, not starting on d
        # but finishing on d or after
        # [multi]allday events have ending dates for the day after their actual ending day
        # so ignore those events if the current date equals their 'uncorrect' ending date
        occurringEvents = list(filter(lambda x: x.start.date() < d <= x.end.date() 
                                                and not ('allday' in x.type and x.end.dateEquals(d)), events))

        # print date label
        print(d.strftime('%d %b, %a'))

        # print occurring events
        if len(occurringEvents) > 0:
            print('[From past days]')

            for e in occurringEvents:
                if d < e.end.date():
                    # event does not end on d
                    printAgendaEvent(e,'mid')
                elif d == e.end.date():
                    # event ends on d
                    printAgendaEvent(e,'end')
            
            if len(startingEvents) > 0:
                print('[New events]')

        # print starting events
        for e in startingEvents:
            printAgendaEvent(e)

        # print newline
        print('') 


def printAgendaEvent(event, when='start'):
    out = '\t'
    if event.type == 'singleday':
        out += '{} - {}\t'.format(event.start.timeStr(), event.end.timeStr())
    elif event.type == 'allday':
        out += 'All day\t\t'
    elif event.type == 'multiallday':
        out += 'All day\t\t'
    elif event.type == 'multiday':
        if when == 'start':
            out += 'From {}\t'.format(event.start.timeStr())
        elif when == 'mid':
            out += 'All day\t\t'
        elif when == 'end':
            out += 'Until {}\t'.format(event.end.timeStr())
    
    out += event.summary
    print(out)