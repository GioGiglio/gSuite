from event import Event
from utils import loadCreds
import reqs

loadCreds()
reqs.init()

e = Event.readEvent()
print(e,'\n---------\n',e.toDict())

#reqs.insertEvent(e)
#print(vars(e))
#print(e.__dict__)


#x = Event('Gerry Scotti','sample description','07/10/2019 9:30','07/10/2019 11:30','Università degli studi di Firenze',None)
#print(x)

#events = reqs.listEvents()
#with open('list.txt','w') as file:
#    for e in events:
#        print(Event.parse(e))
#        for k,v in e.items():
#            file.write(str(k) + ' ' + str(v) + '\n')

#for e in events:
#    print(str(Event.parse(e)))
#    print('\n')
