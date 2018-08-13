from runtrack_app import app
from flask import render_template, url_for, request

@app.route("/register", methods=["GET", "POST"])
def register():
	pass