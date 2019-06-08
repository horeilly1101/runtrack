"""Contains controllers that deal with user accounts"""

from flask_login import logout_user
from runtrack_app.views.forms import LoginForm
from runtrack_app import db
from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_user, current_user
from runtrack_app.views.forms import RegistrationForm
from runtrack_app.models.tables import User

accounts = Blueprint("accounts", __name__)


@accounts.route('/logout')
def logout():
    """route for the logout page. Logs a user out of their account."""
    logout_user()
    return redirect(url_for('login'))


@accounts.route("/login", methods=["GET", "POST"])
def login():
    """route for the login page"""

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

    return render_template("account_routes/login.html", form=form)


@accounts.route("/register", methods=["GET", "POST"])
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

    return render_template("account_routes/register.html", form=form)
