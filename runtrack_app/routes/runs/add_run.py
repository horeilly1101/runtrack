from runtrack_app import app
from flask import render_template, url_for, request
from flask_login import current_user, login_required
# from runtrack_app.forms import AddRunForm

@app.route("/add_run")
@login_required
def add_run():
	# form = AddRunForm()
	return render_template("runs/add_run.html")