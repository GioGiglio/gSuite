from copy import copy
from event import Event
from datetime import timedelta, date


def printAgenda(events,days):
    # start / end should be for the current week
    #maxDate = max(map(lambda x: x.end.date(), events))

    lastDate = None
    startDate = date.today()
    endDate = startDate + timedelta(days=days)
    agenda = {}

    for i in range(days):
        d = startDate + timedelta(days=i)
        occurringEvents = list(filter(lambda x: x.start.date() <= d <= x.end.date(), events))
        if len(occurringEvents) > 0:
            agenda[d] = occurringEvents

    print(agenda)
    print(list(map(lambda x: list(map(lambda y: str(y), x)),agenda.values())))
    return

    for e in events:
        if lastDate and e.start.date() == lastDate:
            # same date
            print(e.str2())
            
        else:
            # new date
            print('')       # print new line
            lastDate = e.start.date()
            print(e.start.strftime('%d %b, %a'))
            print(e.str2())



def printAgenda2(events):
    # expand multi day events

    lastDate = None

    #for e in events:
    #    print('TYPE {}, EVENT: {}'.format(e.type, e))
    
    
    #for i,e in enumerate(events):
    i = 0
    while i < len(events):        
        e = events[i]

        if e.type != 'multiday' and e.type != 'multiallday':
            i+= 1
            continue
        
        daysDiff = (e.end - e.start).days -1

        if daysDiff > 0:
            for j in reversed(range(daysDiff)):
                # create subevent
                # se = dict(event=e, start = e.start + timedelta(days=j+1))

                se = copy(e)
                se.start += timedelta(days=j+1)

                # insert subevent
                events.insert(i,se)
                i += daysDiff
        else:    
            i+= 1
        

    for e in events:
        if lastDate and e.start.date() == lastDate:
            # same date
            print(e.str2())
            
        else:
            # new date
            print('')       # print new line
            lastDate = e.start.date()
            print(e.start.strftime('%d %b, %a'))
            print(e.str2())
