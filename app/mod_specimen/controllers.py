from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from app import login
from app.mod_auth.models import User
from app.mod_package.models import Package, Partner
from app.mod_util.utils import is_safe_url

# Define the blueprint
mod_specimen = Blueprint('specimen', __name__)

@mod_specimen.route('/', methods=['GET'])
@login_required
def index():
    return render_template('specimen/index.html')