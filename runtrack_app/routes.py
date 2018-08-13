from runtrack_app import app
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
	return render_template("base.html")

@app.route("/login")
def login():
	pass