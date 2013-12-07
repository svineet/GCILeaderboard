from pprint import pprint
import requests
from flask import *
app = Flask(__name__)

BASEURL = "http://www.google-melange.com/gci/org/google/gci2013/{orgname}?fmt=json&limit=500&idx=1"

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

	# pprint(final_dict)
	sorted_dict = sorted(final_dict.iteritems(), key=lambda x: x[1], reverse=True)
	# pprint(sorted_dict)
	return render_template("org.html", leaderboard=sorted_dict, org=orgname)


if __name__ == '__main__':
    app.run(host="0.0.0.0")