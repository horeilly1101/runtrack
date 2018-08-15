from runtrack_app import app, db
from flask import render_template, url_for, request, redirect
from flask_login import current_user, login_required
from runtrack_app.forms import AddRunForm
from runtrack_app.models import Run
from datetime import datetime

@app.route("/add_run", methods=["GET", "POST"])
@login_required
def add_run():
	user = current_user
	form = AddRunForm()

	if form.validate_on_submit():
		run = Run(distance=form.distance.data, user_id = user.id)
		start_datetime = datetime.combine(form.start_date.data, form.start_time.data)
		run.started_at = start_datetime
		db.session.add(run)
		db.session.commit()

		return redirect('runs')
	return render_template("runs/add_run.html",
		form=form)