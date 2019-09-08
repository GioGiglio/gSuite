from datetime import date, timedelta, datetime
from reqs import SCOPES
import json
import re

emails = None
emailRegex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
regex = re.compile(emailRegex)

def loadCalendars():
    # read calendars
    with open('calendars.json','r') as f:
        calendars = json.load(f)
    return calendars

def loadEmails():
    global emails
    with open('emails.json','r') as f:
        emails = json.load(f)

def toEmail(name):
    if regex.match(name):
        return name
    
    return emails[name]