import rrule
import json

def test_rrule():
    r = rrule.fromUserInput('20 days')
    print(r)
    r = rrule.toStr(r)
    print(r)
    r = rrule.fromUserInput('1 weeks on mon,thu')
    print(r)
    r = rrule.toStr(r)
    print(r)
    r = rrule.fromUserInput('3 days for 15 times')
    print(r)
    r = rrule.toStr(r)
    print(r)
    r = rrule.fromUserInput('2 weeks on fri until 31 12 2019')
    print(r)
    r = rrule.toStr(r)
    print(r)


def test():
    with(open('emails.json')) as f:
        attendees = json.load(f)

    s = input('with: ')
    names = s.split(' ')

    #emails = list(map(lambda x: x if isEmail(x) else attendees[x] , names))
    emails = list(map(toEmail, names))
    print(emails)

    print(attendees['friends'])
    #'attendees': [
    #    {'email': 'lpage@example.com'},
    #    {'email': 'sbrin@example.com'},
    #]


def toEmail(name):
    with(open('emails.json')) as f:
        emails = json.load(f)

    if isEmail(name):
        return name
    
    email = emails[name]

    if type(email) == list:
        return email
    else:
        return email


def isEmail(s):
    return '@' in s

test()