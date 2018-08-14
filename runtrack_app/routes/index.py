from runtrack_app import app
from flask import render_template, url_for, request
from flask_login import current_user, login_required

@app.route("/")
@app.route("/index")
@login_required
def index():
	return render_template("logged_in/index.html")