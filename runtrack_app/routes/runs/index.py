from runtrack_app import app
from runtrack_app.classes import *
from flask import render_template, url_for, request
from flask_login import current_user, login_required
from datetime import date, datetime, timedelta
import calendar

def name_weeks(monday):
	'''names a week

	kw args:
		monday -- Date object that represents Monday
	'''
	sunday = monday + timedelta(days=6)
	monday_str = calendar.month_abbr[monday.month] + " " + str(monday.day)
	if monday.month == sunday.month:
		return monday_str + " - " + str(sunday.day)
	else:
		sunday_str = calendar.month_abbr[sunday.month] + " " + str(sunday.day)
		return monday_str + " - " + sunday_str

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

	# Get alltime distances
	alltime_ggr = GroupGoalRuns(user.goals, user.runs).weekly(dummy=True, at_least=4)
	alltime_runs = GroupGoalRunsWeekly.weekly_distances(alltime_ggr)

	# Get alltime weekdays
	alltime_weeks = list(map(lambda wggr: name_weeks(wggr.monday), alltime_ggr))

	# Get weekly data
	weekly_runs = alltime_runs[-4:]
	weeks = alltime_weeks[-4:]

	return render_template("runs/index.html", 
		days=days,
		daily_runs=daily_runs,
		weeks=weeks,
		weekly_runs=weekly_runs,
		alltime_weeks=alltime_weeks,
		alltime_runs=alltime_runs)