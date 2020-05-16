from flask import Flask
import json, os, re
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from search import searchData
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

script_dir = os.path.dirname(__file__)
minorFileName = 'minor.json'
minorFileName = os.path.join(script_dir, minorFileName)

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


with open(os.path.join(script_dir, 'data/data.json')) as f:
    profs = list(set(json.load(f).keys()))
    profs.sort()


def fetch_results(prof):
    tb = [[['Monday']], [['Tuesday']], [['Wednesday']], [['Thursday']], [['Friday']]]
    times = ['', '9:30 AM', '11:00 AM', '12:45 PM', '2 PM', '3:30 PM', '5 PM']

    prof = correct_spelling(prof)
    slot_data = get_times(prof)
    dept = get_attr(prof, 'dept')
    website = get_attr(prof, 'website')

    if len(slot_data) == 0 and len(dept) == 0:
        abort(404)

    data = get_table(slot_data)

    for row in tb:
        for i in range(9):
            row.append([])

    for item in data:
        for venue in data[item]:
            if venue == '0':
                venue = 'In Dept'

            tb[int(item[0])][int(item[1])+1].append(venue)

    return [tb, times, dept, website, prof.title()]

@app.route('/professor', methods=['POST'])
def result():
    prof = request.form['prof']
    tb, times, dept, website, prof = fetch_results(prof)
    return render_template('main.html', name=prof, website=website, data=tb, times=times, profs=profs, dept=dept, error=False)

@app.route('/professor', methods=['GET'])
def main():
    prof = request.args.get('prof')

    if prof:
        tb, times, dept, website, prof = fetch_results(prof)
        return render_template('main.html', name=prof, website=website, data=tb, times=times, profs=profs, dept=dept, error=False)

    else:
        return render_template('main.html', profs=profs)      

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))