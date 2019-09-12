# gCal
A command line client for _Google Calendar_ intended for __fast__ events creation and listing.

## Objectives
- __Speed__: The process of events creation or listing is all about speed. Let's take a look at the creation of a _quick event_ :
```
$ gcal -q today 18 30, grocery shopping
-- event added
```
- __Easyness__: It's so easy to define __dates__, __attendees__ or even complex fields like __recurrences__:
```
$ gcal -n
Name: Meeting
Start: next mon 16 00
End: next mon 18 30
Location: Office
Extra fields? (y/n): y
Description:
Recurrence: every 2 weeks for 3 times
With: john micheal william
-- event added
```
	
### How a __date__ is defined:
- `31 12 2019 13 35` represents the 31 December 2019 at 13:35.
- `today|tomorrow` represent the date of today or tomorrow.
- `next mon|tue|wed|thu|fri|sat|sun` represents the date corresponding to the next weekday selected.
- Time can be omitted, for an event lasting all day.


### How a __recurrence__ is defined:
The pattern to follow is : <br>
`every INTERVAL FREQUENCY [on WEEKDAY WEEKDAY ...] for COUNT times | until DATE`
- `INTERVAL`:  an interger between 1 and 99
- `FREQUENCY`: one of `days`,  `weeks`, `months`, `years`
- `WEEKDAY`: one of `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`.
- `COUNT`: an integer between 1 and 99
- `DATE`: the ending date. See how a date is defined for more info.

__Note__: `for` and `until` cannot be used togheter.
	
Examples:
- every 3 weeks
- every 20 days for 5 times
- every 2 weeks on mon fri until 31 12 2019

### How an __attendee__ is defined:
An attende is defined by both an __email address__ or a __name__.
In order to use names, the file `emails.json` should contain the matches between names and emails in the following form:
```
{
	"john": "john@example.com",
	"micheal": "micheal@example.com",
	"william": "william@example.com"
}	
```
Examples:
- john
- john@example.com micheal@example.com
- john micheal otherguy@example.com

__Note__: For more than one attendee, the default separator is `space`
	

