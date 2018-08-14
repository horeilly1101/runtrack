from runtrack_app import app, db
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_user, current_user, login_required
from runtrack_app.forms import RegistrationForm
from runtrack_app.models import User

@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, name=form.name.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()

		login_user(user, remember=form.remember_me.data)
		flash("Welcome to runtrack!")
		return redirect(url_for('index'))

	return render_template("register.html", form=form)