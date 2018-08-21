from runtrack_app import app
from runtrack_app.models import Run, Goal
from runtrack_app.functions import combine_daily_and_weekly, group_runs_daily_and_weekly, \
	sort_runs, group_runs_daily, total_daily_distances, total_combined_distances
from flask import render_template, url_for, request
from flask_login import current_user, login_required
import calendar

@app.route("/runs")
@login_required
def runs():
	user = current_user
	if user.runs:
		weeks = combine_daily_and_weekly(user.runs, user.goals)[::-1]
	else:
		weeks = []

	return render_template("runs/runs.html",
		weeks=weeks,
		month_abbr=calendar.month_abbr,
		day_abbr=calendar.day_abbr,
		total_combined_distances=total_combined_distances)