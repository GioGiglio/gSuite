from event import Event
from utils import readCreds
import reqs

readCreds()
reqs.init()

x = Event('Gerry Scotti','sample description','07/10/2019 9:30','07/10/2019 11:30','Università degli studi di Firenze',None)
print(x)

events = reqs.listEvents()
#with open('list.txt','w') as file:
#    for e in events:
#        print(Event.parse(e))
#        for k,v in e.items():
#            file.write(str(k) + ' ' + str(v) + '\n')

for e in events:
    print(str(Event.parse(e)))
