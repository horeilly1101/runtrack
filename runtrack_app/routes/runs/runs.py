from runtrack_app import app
from runtrack_app.models import Run, Goal
from runtrack_app.classes import *
from flask import render_template, url_for, request
from flask_login import current_user, login_required
from calendar import day_abbr, month_name
from datetime import timedelta

def readable_date(date):
	'''makes a date object more readable

	date -- Date object
	'''
	return month_name[date.month] + " " + str(date.day) + ", " + str(date.year)

@app.route("/runs")
@login_required
def runs(dummy=True):
	user = current_user

	grouped_goalruns = GroupGoalRuns(goals=user.goals, runs=user.runs)
	weeks = grouped_goalruns.weekly()[::-1]

	weekdays = list(map(lambda i: day_abbr[i], range(7)))

	for wggr in weeks:
		print(wggr.daily_distances())

	return render_template("runs/runs.html",
		weeks=weeks,
		float=float,
		len=len,
		readable_date=readable_date)