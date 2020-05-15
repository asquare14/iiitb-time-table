import json, re
import os
script_dir = os.path.dirname(__file__)
dataFileName = 'courses.json'
dataFileName = os.path.join(script_dir, dataFileName)

slotFileName = './slots.1.txt'
slotFileName = os.path.join(script_dir, slotFileName)

def slot2Time(slot):
	with open(slotFileName, 'r') as slotFile:
		for line in slotFile:
			if line.startswith(slot):
				return line.split()[1:]
	return []

def searchData(query):
	with open(dataFileName, 'r') as dataFile:
		data = json.load(dataFile)
	results = [ course for course in data if re.search( query, course['Name'], re.IGNORECASE ) ]
	
	ret = []
	for course in results:
		slots = []
		for slot in course['Data']['Slot'].split(','):
			slots.extend( slot2Time( slot.strip() ) )
		course['Data']['Slot'] = slots
		ret.append(course)

	return ret 

if __name__ == '__main__':
	print( searchData( input('Search for: ') ) )