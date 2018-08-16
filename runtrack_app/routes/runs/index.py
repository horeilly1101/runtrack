from runtrack_app import app
from flask import render_template, url_for, request
from flask_login import current_user, login_required
from datetime import datetime, timedelta
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

	# Get last 7 day totals
	last_week_runs = []
	user_runs = current_user.runs
	user_runs.sort(key = lambda run: run.started_at)
	day = today
	while day > today - timedelta(days=7):
		daily_runs = []
		while len(user_runs) and user_runs[-1].started_at.date() == day:
			daily_runs.append(float(user_runs.pop().distance))
		last_week_runs.append(daily_runs)
		day -= timedelta(days=1)

	last_week_totals = list(map(lambda runs: sum(runs), last_week_runs))
	last_week_totals.reverse()

	print(last_week_runs)

	labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
	values = [10, 9, 8, 7]

	return render_template("runs/index.html", 
		values=values, 
		labels=labels,
		days=days,
		runs=last_week_totals)