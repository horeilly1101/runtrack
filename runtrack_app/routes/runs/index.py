from runtrack_app import app
from runtrack_app.functions import total_daily_distances, total_weekly_distances, sort_runs
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

	# Get daily distances
	daily_runs = total_daily_distances(user.runs, start_date=today - timedelta(days=6))

	# Get last 7 weekdays
	days = []
	for day_int in range(today.weekday()-6, today.weekday()+1):
		day = day_int % 7
		days.append(calendar.day_abbr[day])

	# Get weekly distances (all time)
	alltime_runs = total_weekly_distances(user.runs)

	# Get names of recorded weeks (min 4 weeks)
	if len(alltime_runs) > 3:
		first_date = sort_runs(user.runs)[0].started_at.date()
		first_monday = first_date - timedelta(days=first_date.weekday())
	else:
		first_monday = today - timedelta(days=today.weekday() + 21)
		alltime_runs = [[]] * (4 - len(alltime_runs)) + alltime_runs

	alltime_weeks = []
	monday = first_monday
	while monday <= today:
		interval = "{} {} - ".format(calendar.month_abbr[monday.month], monday.day)
		saturday = monday + timedelta(days=6)
		if monday.month == saturday.month:
			interval += str(saturday.day)
		else:
			interval += "{} {}".format(calendar.month_abbr[saturday.month], saturday.day)
		alltime_weeks.append(interval)
		monday += timedelta(days=7)

	# Get running and name data for last 4 weeks
	weeks = alltime_weeks[-4:]
	weekly_runs = alltime_runs[-4:]

	return render_template("runs/index.html", 
		days=days,
		daily_runs=daily_runs,
		weeks=weeks,
		weekly_runs=weekly_runs,
		alltime_weeks=alltime_weeks,
		alltime_runs=alltime_runs)