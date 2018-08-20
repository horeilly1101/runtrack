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
		goal_check = Goal.query.filter_by(user_id=user.id, date=form.date.data).first()
		if not goal_check:
			goal = Goal(distance=form.distance.data, user_id = user.id, date=form.date.data)
			db.session.add(goal)
			db.session.commit()
			flash('Your goal has been added!')
		else:
			goal_check.distance = form.distance.data
			db.session.add(goal_check)
			db.session.commit()
			flash('Your goal has been updated!')

		return redirect('runs')
	return render_template("runs/add_goal.html",
		form=form)