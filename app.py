from flask import Flask
import json, os, re
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from search import searchData
import os
import itertools
import requests
import json
import re
import sys
import collections



app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
port = int(os.environ.get("PORT", 5000))

script_dir = os.path.dirname(__file__)
minorFileName = 'minor.json'
minorFileName = os.path.join(script_dir, minorFileName)

profs_dict = {}


DEPT_KEY = 'dept'
WEBSITE_KEY = 'website'
TIMETABLE_KEY = 'timetable'


class CaseInsensitiveDict(dict):
    """Basic case insensitive dict with strings only keys."""

    proxy = {}


    def __init__(self, data):
        self.proxy = dict((k.lower(), k) for k in data)
        for k in data:
            self[k] = data[k]


    def __contains__(self, k):
        return k.lower() in self.proxy


    def __delitem__(self, k):
        key = self.proxy[k.lower()]
        super(CaseInsensitiveDict, self).__delitem__(key)
        del self.proxy[k.lower()]


    def __getitem__(self, k):
        key = self.proxy[k.lower()]
        return super(CaseInsensitiveDict, self).__getitem__(key)


    def get(self, k, default=None):
        return self[k] if k in self else default


    def __setitem__(self, k, v):
        super(CaseInsensitiveDict, self).__setitem__(k, v)
        self.proxy[k.lower()] = k


class SpellingCorrector():
    """
        Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html
        Copyright (c) 2007-2016 Peter Norvig
        MIT license: www.opensource.org/licenses/mit-license.php
    """


    word_list = []
    WORDS = collections.Counter([])


    def __init__(self, words):
        self.word_list = [t.lower() for t in words]
        self.WORDS = collections.Counter(self.word_list)


    def P(self, word, N=sum(WORDS.values())):
        "Probability of `word`."
        if N == 0:
            return 0
        return self.WORDS[word] / N


    def correction(self, word):
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.P)


    def candidates(self, word):
        "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])


    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.WORDS)


    def edits1(self, word):
        "All edits that are one edit away from `word`."

        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]

        return set(deletes + transposes + replaces + inserts)


    def edits2(self, word):
        "All edits that are two edits away from `word`."

        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))





with open(os.path.join(script_dir, 'data/data.json'), 'r') as f:
    profs_dict = CaseInsensitiveDict(json.load(f))




def get_times(prof_name):
    data = CaseInsensitiveDict(profs_dict)
    result = []

    try:

        result = data[prof_name][TIMETABLE_KEY]

        if result:
            result.sort()
            result = list(result for result, _ in itertools.groupby(result))

    except:

        pass

    return result

def get_table(details):
    tb = {}

    for i in range(5):
        for j in range(9):
            tb.update({'%d%d' % (i, j): []})

    for times, venues in details:
        venues = set(v.strip() for v in venues)

        for time in times:
            tb[time] = venues

    return tb


def get_attr(prof_name, key):
    data = CaseInsensitiveDict(profs_dict)
    result = ""

    try:

        result = data[prof_name][key]

    except:

        pass


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
    times = ['', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '2 PM', '3 PM', '4 PM', '5 PM']

    prof = correct_spelling(prof)
    slot_data = get_times(prof)
    dept = get_attr(prof, 'dept')
    website = get_attr(prof, 'website')
    print(prof, slot_data, dept, website)

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

def correct_spelling(prof_name):
	prof_names = profs_dict.keys()
	if prof_name not in prof_names:
		corrector = SpellingCorrector(prof_names)
		return corrector.correction(prof_name)
	return prof_name

@app.route('/professor', methods=['POST'])
def result():
    prof = request.form['prof']
    tb, times, dept, website, prof = fetch_results(prof)
    print(prof)
    return render_template('main.html', name=prof, website=website, data=tb, times=times, profs=profs, dept=dept, error=False)

@app.route('/professor', methods=['GET'])
def main():
    prof = request.args.get('prof')
    print(prof)
    if prof:
        print("hola")

        tb, times, dept, website, prof = fetch_results(prof)
        return render_template('main.html', name=prof, website=website, data=tb, times=times, profs=profs, dept=dept, error=False)

    else:
        return render_template('main.html', profs=profs) 


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))