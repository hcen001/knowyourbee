from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from app import login
from app.mod_auth.models import User
from app.mod_sample.models import Sample
from app.mod_util.utils import is_safe_url

# Define the blueprint
mod_sample = Blueprint('sample', __name__)

@mod_sample.route('/', methods=['GET'])
@login_required
def index():
    return render_template('sample/index.html')