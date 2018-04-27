from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from app import login
from app.mod_auth.models import User
from app.mod_package.models import Package, Partner
from app.mod_util.utils import is_safe_url

## commenting this exception helps debugging when there are issues with importing
@login.user_loader
def load_user(id):
    # try:
    return User.query.filter(User.id == int(id)).first()
    # except User.DoesNotExist:
        # return None

# Define the blueprint
mod_specimen = Blueprint('specimen', __name__)

@mod_specimen.route('/', methods=['GET'])
@login_required
def index():
    return render_template('specimen/index.html')