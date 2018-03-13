from flask import Blueprint, redirect, url_for, abort
from app import login
from app.mod_auth.models import User
from flask_login import login_required, current_user, logout_user

@login.user_loader
def load_user(id):
    try:
        return User.query.filter(User.id == int(id)).first()
    except User.DoesNotExist:
        return None

# Define the blueprint: 'auth', set its url prefix: app.url/auth
entry_point = Blueprint('dashboard', __name__)

# Set the route and accepted methods
@entry_point.route('/', methods=['GET'])
def index():
    try:
        return redirect(url_for('dashboard.dashboard'))
    except Exception as e:
        raise e
        abort(404)

@entry_point.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard/index.html', title=Dashboard)

@entry_point.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.logout()
    logout_user()
    return redirect(url_for('dashboard.index'))
