from datetime import date, timedelta, datetime
from reqs import SCOPES
import json

def loadCalendars():
    # read calendars
    with open('calendars.json','r') as f:
        calendars = json.load(f)
    return calendars
