from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from app import login
from app.mod_package.models import Package, Partner
from app.mod_auth.models import User
from app.mod_util.utils import is_safe_url

@login.user_loader
def load_user(id):
    try:
        return User.query.filter(User.id == int(id)).first()
    except User.DoesNotExist:
        return None

# Define the blueprint
mod_package = Blueprint('package', __name__)

@mod_package.route('/', methods=['GET'])
def index():
    return render_template('package/index.html')
