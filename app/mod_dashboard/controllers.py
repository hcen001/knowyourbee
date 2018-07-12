from flask import Blueprint, redirect, url_for, abort, render_template, render_template_string
from app import login
from app.mod_auth.models import User
from app.mod_package.models import Package
from flask_login import login_required, current_user

@login.user_loader
def load_user(id):
    try:
        return User.query.filter(User.id == int(id)).first()
    except User.DoesNotExist:
        return None

# Define the blueprint
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
    js = render_template('dashboard/index.js')
    stats = Package.stats()
    return render_template('dashboard/index.html', title='Dashboard', user=current_user, js=js, stats=stats)
