# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
from jinja2 import TemplateNotFound

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import module forms
from app.mod_auth.forms import LoginForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    logged_in = False
    if logged_in is False:
        form = LoginForm(request.form)
        try:
            return render_template('auth/login.html', form=form)
        except TemplateNotFound as e:
            print(e)
            abort(404)
    return 'Hello, world!'
