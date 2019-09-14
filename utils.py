import json
import re

namesToEmails = None
emailsToNames = None
emailRegex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
regex = re.compile(emailRegex)

def loadCalendars():
    # read calendars
    with open('calendars.json','r') as f:
        calendars = json.load(f)
    return calendars

def loadEmails():
    global namesToEmails
    global emailsToNames
    with open('emails.json','r') as f:
        namesToEmails = json.load(f)
    emailsToNames = {v:k for k,v in namesToEmails.items()}

def toEmail(name):
    if regex.match(name):
        return name
    
    return namesToEmails[name]

def parseAttendees(s):
    names = s.split(' ')

    emails = list(map(toEmail, names))
    return emails

def nameFromEmail(email):
    # returns the name associated with the email, if existing.
    # Otherwise returns the email
    try:
        return emailsToNames[email]
    except KeyError:
        return email