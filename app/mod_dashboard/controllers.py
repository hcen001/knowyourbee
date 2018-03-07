from flask import Blueprint, redirect, url_for, abort

# Define the blueprint: 'auth', set its url prefix: app.url/auth
entry_point = Blueprint('dashboard', __name__)

# Set the route and accepted methods
@entry_point.route('/', methods=['GET'])
def signin():
    print('Sign in')
    logged_in = False
    if logged_in is False:
        try:
            return redirect(url_for('auth.signin'))
        except Exception as e:
            raise e
            abort(404)
    return 'Hello, world!'