from imports import *
from prof import *
from calendarfunc import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
port = int(os.environ.get("PORT", 5000))

script_dir = os.path.dirname(__file__)
minorFileName = 'course_list.json'
minorFileName = os.path.join(script_dir, minorFileName)


@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		data = request.json
		return download_ics_file(data)
		return jsonify(data)
	return render_template('home.html')

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

@app.route('/professor', methods=['POST'])
def result():
	prof = request.form['prof']
	tb, times, dept, website, prof, course = fetch_results(prof)
	return render_template('main.html', name=prof, website=website, data=tb, times=times, profs=profs, dept=dept,course=course, error=False)

my_events = []

@app.route('/professor', methods=['GET'])
def main():
	global my_events
	prof = request.args.get('prof')
	if prof:
		tb, times, dept, website, prof, course = fetch_results(prof)
		my_events = format_data(tb)
		print(my_events)
		return render_template('main.html', name=prof, website=website, data=tb, times=times, profs=profs, dept=dept,course=course, error=False)
	else:
		return render_template('main.html', profs=profs) 

@app.route('/ics_helper')
def ics_helper():
	print(my_events)
	return download_ics_file(my_events)

@app.route("/getPlotCSV")
def getPlotCSV():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})

if __name__ == '__main__':

	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
