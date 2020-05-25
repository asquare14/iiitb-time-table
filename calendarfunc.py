from imports import *

script_dir = os.path.dirname(__file__)

c = Calendar()

timeMapStart = {}
timeMapEnd = {}
timeMapStart[0] = "09:30:00"
timeMapEnd[0] = "11:00:00"
timeMapStart[1] = "11:15:00"
timeMapEnd[1] = "12:45:00"
timeMapStart[2] = "14:00:00"
timeMapEnd[2] = "15:30:00"
timeMapStart[3] = "15:45:00"
timeMapEnd[3] = "17:15:00"

def format_data(data):
	today = date.today()
	day = today.weekday()
	my_events = []
	for i in range(len(data)):
		for j in range(1, len(data[i])):
			numberOfDaysToAdd = 0
			if i < day:
				numberOfDaysToAdd = i + 7 - day
			else:
				numberOfDaysToAdd = i - day
			if(len(data[i][j])):
				temp = []
				thisday = today + timedelta(days = numberOfDaysToAdd)
				temp.append(data[i][j][0])
				temp.append(thisday.strftime("%Y-%m-%d") + " " + timeMapStart[j - 1])
				temp.append(thisday.strftime("%Y-%m-%d") + " " + timeMapEnd[j - 1])
				my_events.append(temp)
	my_events.sort()
	return my_events


def download_ics_file(my_events):
	for event in my_events:
		e = Event()
		e.name = event[0]
		e.begin = event[1]
		e.end = event[2]
		c.events.add(e)
		c.events

	return Response(c, mimetype="text/calendar", headers={"Content-disposition": "attachment; filename=schedule.ics"})


