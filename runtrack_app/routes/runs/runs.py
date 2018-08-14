from runtrack_app import app
from flask import render_template, url_for, request
from flask_login import current_user, login_required

@app.route("/<name>'s-runs")
@login_required
def runs(name):
	return render_template("runs/runs.html")