from runtrack_app import app, db
from flask import render_template, url_for, request, redirect, flash
from flask_login import current_user, login_required
from runtrack_app.forms import AddGoalForm
from runtrack_app.models import Run, Goal
from datetime import datetime

@app.route("/add_goal", methods=["GET", "POST"])
@login_required
def add_goal():
	user = current_user
	form = AddGoalForm()

	if form.validate_on_submit():
		goal = Goal(distance=form.distance.data, user_id = user.id, date=form.date.data)
		db.session.add(goal)
		db.session.commit()

		flash('Your goal has been added!')
		return redirect('runs')
	return render_template("runs/add_goal.html",
		form=form)