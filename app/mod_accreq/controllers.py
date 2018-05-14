from flask import Blueprint, request, render_template, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user

from app.mod_auth.models import AccountRequest

import json


# Define the blueprint
mod_accreq = Blueprint('accreq', __name__)

@mod_accreq.route('/', methods=['GET'])
@login_required
def index():
    js = render_template('accreq/index.js')
    return render_template('accreq/index.html', user=current_user, title='Account Request', js=js)

@mod_accreq.route('/all', methods=['GET'])
@login_required
def accreqs():
    data = AccountRequest.accreqs_datatable()
    output = {'data': data}
    return jsonify(output)