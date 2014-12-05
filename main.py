import requests
import os
from datetime import datetime
from flask import *
app = Flask(__name__)

BASEURL = "http://www.google-melange.com/gci/org/google/gci2014/" \
    "{orgname}?fmt=json&limit=500&idx=1"

orglist = ['sugarlabs',
           'mifos',
           'apertium',
           'brlcad',
           'sahana',
           'copyleftgames',
           'openmrs',
           'wikimedia',
           'kde',
           'haiku',
           'drupal',
           'fossasia']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/student/<name>-count=<int:e>-org=<org>')
def student(name, e=0, org=None):
    tasks = []
    total = 0

    ol = orglist
    if org and u'All' not in org:
        ol = [org] + ol

    for org in ol:
        page_url = BASEURL.format(orgname=org)
        page = requests.get(page_url)
        page_json = page.json

        data = page_json['data']['']
        for row in data:
            student_name = row['columns']['student']
            if student_name == name:
                total += 1
                student_name = row['columns']['student']
                title = row['columns']['title']
                link = "http://www.google-melange.com" + \
                    row['operations']['row']['link']
                type_ = row['columns']['types']
                tasks.append((title, link, type_, org))
            tasks.sort()
            if total == e and e:
                return render_template("student.html",
                                       tasks=tasks,
                                       total=total,
                                       name=name)
    # tasks.sort(key=lambda x: (x[0], x[2], x[3], x[0]))
    return render_template("student.html", tasks=tasks,
                           total=total,
                           name=name)


@app.route('/org/<org>/')
def leaderboard(org):
    orgname = org
    page_url = BASEURL.format(orgname=orgname)
    page = requests.get(page_url)
    page_json = page.json
    final_dict = {}

    data = page_json['data']['']
    for row in data:
        student_name = row['columns']['student']
        if student_name in final_dict:
            final_dict[student_name] += 1
        else:
            final_dict[student_name] = 1

    sorted_dict = sorted(final_dict.iteritems(), key=lambda x: x[1],
                         reverse=True)

    total = sum([int(tup[1]) for tup in final_dict.iteritems()])
    total_students = len(set([tup[0] for tup in final_dict.iteritems()]))
    return render_template("org.html", leaderboard=sorted_dict,
                           org=orgname,
                           total=total,
                           students=total_students)


@app.route('/all/')
def allorgs():
    final_dict = {}

    for org in orglist:
        page_url = BASEURL.format(orgname=org)
        page = requests.get(page_url)
        page_json = page.json

        data = page_json['data']['']
        for row in data:
            student_name = row['columns']['student']
            if student_name in final_dict:
                final_dict[student_name] += 1
            else:
                final_dict[student_name] = 1

    sorted_dict = sorted(final_dict.iteritems(), key=lambda x: x[1],
                         reverse=True)
    total = sum([int(tup[1]) for tup in final_dict.iteritems()])
    total_students = len(set([tup[0] for tup in final_dict.iteritems()]))
    return render_template("org.html", leaderboard=sorted_dict,
                           org="All Organizations",
                           total=total,
                           students=total_students)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
