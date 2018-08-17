from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, TimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')

class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember me')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AddRunForm(FlaskForm):
    distance = StringField('distance', validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    start_time = TimeField('Start date', validators=[DataRequired()])

class AddGoalForm(FlaskForm):
    distance = StringField('distance', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])