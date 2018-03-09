# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
from jinja2 import TemplateNotFound
from flask_login import current_user, login_user

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import module forms
from app.mod_auth.forms import LoginForm, ForgotPasswordForm
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__)

# Set the route and accepted methods
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('User {} already authenticated'.format(current_user.email))
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    forgot_password_form = ForgotPasswordForm()
    if request.method == 'POST':
        print('Request values: ', request.values)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth.login'))
            user.authenticate()
            login_user(user, remember=form.remember_me.data)
            flash('Successful authentication for: {}'.format(user.email))
            return redirect(url_for('dashboard.index'))
        if forgot_password_form.validate_on_submit():
            print('ForgotPasswordForm')
    return render_template('auth/login.html', title='Sign In', form=form, forgot_pw=forgot_password_form)
