from datetime import date, timedelta
s = 'next friday'

weekdays = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

def parse(s):
    s = s.strip()

    if s.startswith('next'):
        day = s.split(' ')[1]
        dayNumber = weekDayNumber(day)
        

def weekDayNumber(day):
    for k,v in weekdays.items():
        if v == day.capitalize():
            return k

    return None

def daysDiff():
    today = date.today()
    currentDayNumber = today.weekday()
    dayNumber = 4 # friday

    if dayNumber <= currentDayNumber:
        days = 7 - currentDayNumber
        days += dayNumber % 7
    else:
        days = dayNumber - currentDayNumber

    print('daysDiff',days)
    nextDate = today + timedelta(days=days)
    print(nextDate)


d1 = weekDayNumber('mon')
d2= weekDayNumber('mongdeas')

if d2 is None:
    print('d2 is not valid')