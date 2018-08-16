from runtrack_app import app
from runtrack_app.functions import sort_runs, group_runs, total_daily_distances
from flask import render_template, url_for, request
from flask_login import current_user, login_required
from datetime import date, datetime, timedelta
import calendar

@app.route("/")
@app.route("/index")
@login_required
def index():
	today = datetime.today().date()

	# Get last 7 weekdays
	days = []
	for day_int in range(today.weekday()-6, today.weekday()+1):
		day = day_int % 7
		days.append(calendar.day_abbr[day])

	# Get daily distances
	runs = total_daily_distances(current_user.runs, start_date=today - timedelta(days=6))

	labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
	values = [10, 9, 8, 7]

	return render_template("runs/index.html", 
		values=values, 
		labels=labels,
		days=days,
		runs=runs)
