from runtrack_app import app
from runtrack_app.models import Run, Goal
from runtrack_app.functions import combine_daily, group_runs_daily_and_weekly, \
	sort_runs, group_runs_daily, total_daily_distances
from flask import render_template, url_for, request
from flask_login import current_user, login_required
import calendar

@app.route("/runs")
@login_required
def runs():
	user = current_user

	# get goals and runs
	goals_runs = combine_daily(user.runs, user.goals)
	goals_runs.reverse()

	return render_template("runs/runs.html",
		goals_runs=goals_runs,
		month_abbr=calendar.month_abbr,
		day_abbr=calendar.day_abbr)