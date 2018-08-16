from runtrack_app import app
from flask import render_template, url_for, request
from flask_login import current_user, login_required

@app.route("/")
@app.route("/index")
@login_required
def index():
	legend = 'Monthly Data'
	labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
	values = [10, 9, 8, 7, 6, 4, 7, 20]

	days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	runs = [1, 2, 3, 4, 5, 6, 7]

	return render_template("runs/index.html", values=values, labels=labels, legend=legend,
		days=days,
		runs=runs)