# Import flask dependencies
from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from jinja2 import TemplateNotFound
from flask_login import current_user, login_user

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import module forms
from app.mod_auth.forms import LoginForm, ForgotPasswordForm, RequestAccountForm
from app.mod_auth.models import User, AccountRequest
from app.mod_util.utils import is_safe_url

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__)

# Set the route and accepted methods
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('User {} already authenticated'.format(current_user.email))
        return redirect(url_for('dashboard.index'))

    login_form = LoginForm(request.form)
    forgot_password_form = ForgotPasswordForm()
    request_form = RequestAccountForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user is None or not user.check_password(login_form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth.login'))
            user.authenticate()
            login_user(user, remember=login_form.remember_me.data)
            _next = request.args.get('next')
            if not is_safe_url(_next):
                return abort(400)
            return redirect(_next or url_for('dashboard.index'))
    return render_template('auth/login.html', title='Sign In', login_form=login_form, forgot_pw=forgot_password_form, request_form=request_form)

@mod_auth.route('/forgotpassword/', methods=['POST'])
def forgotpassword():

    if current_user.is_authenticated:
        flash('Authenticated users cannot request password reset')
        return redirect(url_for('dashboard.index'))

    form = ForgotPasswordForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.recover_email.data).first()
            if user is None:
                flash('Invalid email')
                return redirect(url_for('auth.login'))
            user.forgot_password()
            flash('An email has been sent to {}'.format(user.email))
            return redirect(url_for('dashboard.index'))

@mod_auth.route('/requestaccount/', methods=['POST'])
def requestaccount():

    if current_user.is_authenticated:
        flash('Authenticated users cannot request accounts')
        return redirect(url_for('dashboard.index'))

    request_form = RequestAccountForm(request.form)
    print("form data: ", request_form.data)
    if request.method == 'POST':
        if request_form.validate_on_submit():
            pending = AccountRequest.query.filter(AccountRequest.email==request_form.request_email.data, AccountRequest.granted==False).first()
            if not pending:
                fname = request_form.fname.data
                lname = request_form.lname.data
                email = request_form.request_email.data
                password = request_form.request_password.data
                account_request = AccountRequest(email, password, fname, lname)
                account_request.request()
                flash('Account requested. You should receive an email with your credentials soon.')
            flash('There is a pendinr request for an account with this email.')
        else:
            flash('Invalid form data')
        return redirect(url_for('auth.login'))
