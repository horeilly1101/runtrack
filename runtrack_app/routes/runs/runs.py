from runtrack_app import app
from flask import render_template, url_for, request
from flask_login import current_user, login_required
from runtrack_app.models import Run

@app.route("/runs")
@login_required
def runs():
	user = current_user

	# Sort runs
	user_runs = user.runs
	user_runs.sort(key = lambda run: run.started_at)
	return render_template("runs/runs.html",
		user_runs=user_runs)