from event import Event
from date import Date
import copy
from datetime import timedelta

e1 = Event('summary','description',Date.new(2019,9,15,0,0,False),Date.new(2019,9,15,0,0,False),None,None,None)
e2 = copy.copy(e1)

print(e1 == e2)     # True
print(e1 is e1)     # False

e2.start += timedelta(days=10)

print(e1)
print(e2)