from copy import copy
from event import Event
from datetime import timedelta, date


def printAgenda(events, startDate, days):
    
    for i in range(days):
        d = startDate + timedelta(days=i)
        
        # startingEvents are the events having starting date equal to d
        startingEvents = list(filter(lambda x: x.start.date() == d, events))

        # occurringEvents are the events that last more than one day, not starting on d
        # but finishing on d or after 
        # [multi]allday events have ending dates for the day after their actual ending day
        # so ignore those events if the current date equals their 'uncorrect' ending date
        occurringEvents = list(filter(lambda x: x.start.date() < d <= x.end.date() 
                                                and not ('allday' in x.type and x.end.date() == d), events))

        # print date label
        print(d.strftime('%d %b, %a'))

        # print occurring events
        if len(occurringEvents) > 0:
            print('\t----Events from the past days----')

            if d.day == 19:
                print(occurringEvents[0].str2())

            for e2 in occurringEvents:
                if d < e2.end.date():
                    # at the current day, the event has not finished
                    print(e2.str2('mid'))
                elif d == e2.end.date():
                    # the current date d is the last day of the event
                    print(e2.str2('end'))
            
            if len(startingEvents) > 0:
                print('\t----Events starting ' + d.strftime('%d/%m') + '----')

        # print starting events
        for e1 in startingEvents:
            print(e1.str2())





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
