from runtrack_app import app
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_user, current_user, login_required, logout_user

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))