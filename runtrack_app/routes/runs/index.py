from runtrack_app import app
from flask import render_template, url_for, request
from flask_login import current_user, login_required

@app.route("/")
@app.route("/index")
@login_required
def index():
	legend = 'Monthly Data'
	labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
	values = [10, 9, 8, 7]

	days = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
	runs = [1, 2, 3, 4, 5, 6, 7]

	return render_template("runs/index.html", values=values, labels=labels, legend=legend,
		days=days,
		runs=runs)