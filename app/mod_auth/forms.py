from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember')
    # submit = SubmitField('Sign In')

class ForgotPasswordForm(FlaskForm):
    recover_email = StringField('Email', validators=[DataRequired()])
    # submit = SubmitField('Submit')
