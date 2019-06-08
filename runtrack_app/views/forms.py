"""
Contains form classes:
    LoginForm: login form
    RegistrationForm: registration form
    AddRunForm: adds a run
    AddGoalForm: adds a goal
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from runtrack_app.models.tables import User


class LoginForm(FlaskForm):
    """Form that takes care of user login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')


class RegistrationForm(FlaskForm):
    """Form that takes care of user registration"""
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember me')

    @staticmethod
    def validate_email(email):
        """validate the email field of the RegistrationForm

        :param email: email input by user
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("There is already an account under this email.")


class AddRunForm(FlaskForm):
    """Form that allows a user to add a run"""
    distance = StringField('distance', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])


class AddGoalForm(FlaskForm):
    """Form that allows a user to add a goal."""
    distance = StringField('distance', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
