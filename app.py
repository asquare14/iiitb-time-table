from imports import *
from prof import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
port = int(os.environ.get("PORT", 5000))

script_dir = os.path.dirname(__file__)
minorFileName = 'course_list.json'
minorFileName = os.path.join(script_dir, minorFileName)


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
				temp.append(data[i][j])
				temp.append(thisday.strftime("%Y-%m-%d") + " " + timeMapStart[j - 1])
				temp.append(thisday.strftime("%Y-%m-%d") + " " + timeMapEnd[j - 1])
				my_events.append(temp)
	my_events.sort()
	return my_events


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/search/')
def search():
	query = request.args.get('term')
	results = searchData(query)
	return json.dumps( [ course['Name'] for course in results ] )

@app.route('/ajax/', methods=['POST'])
def getCourse():
	query = request.form.get('query')
	results = searchData(query)
	if results:
		return json.dumps( results[0] )
	else:
		return json.dumps( {} )

@app.route('/minor/')
def minor():
	with app.open_resource(minorFileName, 'r') as minorFile:
		data = json.load(minorFile)
	return json.dumps( data )
	app.run(host='0.0.0.0', port=port, debug=True)

@app.route('/professor', methods=['POST'])
def result():
	prof = request.form['prof']
	tb, times, dept, website, prof, course = fetch_results(prof)
	return render_template('main.html', name=prof, website=website, data=tb, times=times, profs=profs, dept=dept,course=course, error=False)

@app.route('/professor', methods=['GET'])
def main():
	prof = request.args.get('prof')
	if prof:
		tb, times, dept, website, prof, course = fetch_results(prof)
		my_events = format_data(tb)
		print(my_events)
		return render_template('main.html', name=prof, website=website, data=tb, times=times, profs=profs, dept=dept,course=course, error=False)
	else:
		return render_template('main.html', profs=profs) 

if __name__ == '__main__':

	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
