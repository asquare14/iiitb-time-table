from flask import Flask
import json, os, re
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.search import searchData

minorFileName = '/home/atibhi/flask-tutorial/flaskr/minor.json'

bp = Blueprint("blog", __name__, url_prefix="/")

@bp.route('/')
def home():
	return render_template('home.html')

@bp.route('/search/')
def search():
	query = request.args.get('term')
	results = searchData(query)
	return json.dumps( [ course['Name'] for course in results ] )

@bp.route('/ajax/', methods=['POST'])
def getCourse():
	query = request.form.get('query')
	results = searchData(query)
	if results:
		return json.dumps( results[0] )
	else:
		return json.dumps( {} )

@bp.route('/minor/')
def minor():
	with bp.open_resource(minorFileName, 'r') as minorFile:
		data = json.load(minorFile)
	return json.dumps( data )

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)