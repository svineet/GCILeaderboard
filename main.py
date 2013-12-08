from pprint import pprint
import requests
from flask import *
app = Flask(__name__)

BASEURL = "http://www.google-melange.com/gci/org/google/gci2013/{orgname}?fmt=json&limit=500&idx=1"

orglist = ['sugarlabs2013',
		'sahana',
		'apertium',
		'brlcad',
		'copyleftgames',
		'rtems',
		'wikimedia',
		'kde',
		'haiku',
		'drupal']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/org/<org>/')
def leaderboard(org):
	orgname = org
	page_url = BASEURL.format(orgname=orgname)
	page = requests.get(page_url)
	page_json = page.json()

	final_dict = {}

	data = page_json['data']['']
	for row in data:
		student_name = row['columns']['student']
		if student_name in final_dict:
			final_dict[student_name] += 1
		else:
			final_dict[student_name] = 1

	sorted_dict = sorted(final_dict.iteritems(), key=lambda x: x[1], reverse=True)

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
		page_json = page.json()

		data = page_json['data']['']
		for row in data:
			student_name = row['columns']['student']
			if student_name in final_dict:
				final_dict[student_name] += 1
			else:
				final_dict[student_name] = 1

	sorted_dict = sorted(final_dict.iteritems(), key=lambda x: x[1], reverse=True)
	total = sum([int(tup[1]) for tup in final_dict.iteritems()])
	total_students = len(set([tup[0] for tup in final_dict.iteritems()]))
	return render_template("org.html", leaderboard=sorted_dict, 
							org="All Organizations", 
							total=total,
							students=total_students)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")