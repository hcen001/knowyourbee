from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember')

class ForgotPasswordForm(FlaskForm):
    recover_email = StringField('Email', validators=[DataRequired()])

class RequestAccountForm(FlaskForm):
    fname = StringField('First name', validators=[DataRequired()])
    lname = StringField('Last name', validators=[DataRequired()])
    request_email = StringField('Email', validators=[DataRequired()])
    request_password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Re-type password')
    accept_tos = BooleanField('I agree to the Terms of Service & Privacy Policy', [DataRequired()])
