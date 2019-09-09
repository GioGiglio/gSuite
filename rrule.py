from date import Date
from datetime import datetime

def toStr(s):
    # returns a human readable representation of the recurrence
    # "every 2 weeks on FR for 20 times"
    tokens = s.split(';')
    count = None
    interval = None
    until = None
    byday = None
    out = []

    weekdays = {'MO':'Mon', 'TU':'Tue', 'WE':'Wed', 'TH':'Thu', 'FR':'Fri', 'SA':'Sat', 'SU':'Sun'}

    for t in tokens:
        k,v = t.split('=')
        if k =='RRULE:FREQ':
            freq = v
            if freq == 'DAILY':
                freq = 'days'
            elif freq == 'WEEKLY':
                freq = 'weeks'
            elif freq == 'MONTHLY':
                freq = 'months'
            else:
                freq = 'years'

        elif k == 'WKST':
            continue
        elif k == 'COUNT':
            count = v
        elif k == 'INTERVAL':
            interval = v
        elif k == 'UNTIL':
            until = v
            until = datetime.strptime(v,'%Y%m%dT%H%M%SZ').strftime('%d/%m/%Y')
        elif k == 'BYDAY':
            byday = v
    
    if not interval:
        interval = 1

    out.append('every {} {}'.format(interval,freq))

    if byday:
        days = byday.split(',')
        byday = ','.join(map(lambda x: weekdays[x],days))
        out.append('on ' + byday)

    if count:
        out.append('for ' + count + ' times')
    elif until:
        out.append('until ' + until)

    return ' '.join(out)


def _parseTokens(tokens):
    # return order freq, interval, byday, count, until
    freq = None
    interval = None
    byday = None
    count = None
    until = None

    l = len(tokens) -1

    i = 1   # skip tokens[0] that is 'every'
    interval = tokens[i]
    i += 1
    freq = tokens[i]
    i += 1

    #print('i: {}, l: {}, tokens: {}'.format(i,l,tokens))

    if i > l:
        return (freq,interval,byday,count,until)

    if tokens[i] == 'on':
        i += 1
        byday = tokens[i]
        i += 1

    if i > l:
        return (freq,interval,byday,count,until)

    if tokens[i] == 'for':
        i += 1
        count = tokens[i]
    elif tokens[i] == 'until':
        i += 1
        until = ' '.join(tokens[i:i+3])

    return (freq,interval,byday,count,until)

def fromUserInput(s):
    # parses the user input for a recurrence into a string representing the recurrence itself

    tokens = s.split(' ')
    freqs = {'days': 'DAILY', 'weeks': 'WEEKLY', 'months': 'MONTHLY', 'years': 'YEARLY'}
    out = []

    if len(tokens) < 3:
        raise Exception('Invalid format')

    freq,interval,byday,count,until = _parseTokens(tokens)

    # freq
    if freq not in freqs:
        raise Exception('Invalid frequency: ',freq)
    out.append('RRULE:FREQ=' + freqs[freq])

    # interval
    if interval is None:
        raise Exception('Missing INTERVAL parameter')
    out.append('INTERVAL=' + interval)

    # count
    if count is not None:
        out.append('COUNT=' + count)

    # until
    if until is not None:
        try:
            d = Date.fromUserInput(until)
            d = d.strftime('%Y%m%dT%H%M%SZ')
            out.append('UNTIL=' + d)
        except Exception as e:
            print(e)

    # byday
    if byday is not None:
        out.append('WKST=SU')
        days = byday.split(',')
        byday = ','.join(map(lambda x: x[:-1].upper(),days))

        out.append('BYDAY=' + byday)

    return ';'.join(out)