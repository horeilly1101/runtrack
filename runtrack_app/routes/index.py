from runtrack_app import app
from flask import render_template, url_for, request

@app.route("/")
@app.route("/index")
def index():
	return render_template("login.html")