from runtrack_app import app
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_user, current_user, login_required
from runtrack_app.forms import LoginForm
from runtrack_app.models import User

@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid email or password')
			return redirect(url_for('login'))
			
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template("login.html", form=form)