from imports import *

script_dir = os.path.dirname(__file__)

profs_dict = {}


DEPT_KEY = 'dept'
WEBSITE_KEY = 'website'
TIMETABLE_KEY = 'timetable'
COURSE_KEY = 'course'

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


with open(os.path.join(script_dir, 'prof_data.json'), 'r') as f:
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


with open(os.path.join(script_dir, 'prof_data.json')) as f:
    profs = list(set(json.load(f).keys()))
    profs.sort()


def fetch_results(prof):
    tb = [[['Monday']], [['Tuesday']], [['Wednesday']], [['Thursday']], [['Friday']]]
    times = ['', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '2 PM', '3 PM', '4 PM', '5 PM']
    slot_data = get_times(prof)
    dept = get_attr(prof, 'dept')
    website = get_attr(prof, 'website')
    course = profs_dict[prof]['course']    

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

    return [tb, times, dept, website, prof.title(), course]