from runtrack_app import app
from runtrack_app.classes import *
from flask import render_template, url_for, request
from flask_login import current_user, login_required
from datetime import date, datetime, timedelta
import calendar

@app.route("/")
@app.route("/index")
@login_required
def index():
	user = current_user
	today = date.today()
	runs = Runs(user.runs)

	# Get last week runs distances
	week_ago = today - timedelta(days=6)
	daily_runs = runs.daily_distances_between(week_ago, today)

	# Get last 7 weekdays
	days = []
	for day_int in range(today.weekday()-6, today.weekday()+1):
		day = day_int % 7
		days.append(calendar.day_abbr[day])

	# Get weekly distances
	alltime_runs = GroupGoalRuns(user.goals, user.runs).weekly()
	# alltime_runs = list(map)

	return render_template("runs/index.html", 
		days=days,
		daily_runs=daily_runs,
		weeks=weeks,
		weekly_runs=weekly_runs,
		alltime_weeks=alltime_weeks,
		alltime_runs=alltime_runs)