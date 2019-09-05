from event import Event
import utils
import reqs

reqs.init()

calendars = utils.loadCalendars()

e = Event.readEvent()
options = []
for i,v in enumerate(calendars):
    options.append('{}: {}'.format(i,v))

print('Calendar (', end='')
print(*options, sep=', ', end='')
print('): ', end='')
i = input()


#for i,v in enumerate(calsendars):
#    print('{}: {}'.format(i,v))


#reqs.insertEvent(e,)
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
#    print(Event.parse(e))
#    print('\n')
