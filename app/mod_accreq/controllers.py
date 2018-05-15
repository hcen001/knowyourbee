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

@mod_accreq.route('/approveAccount/<accid>', methods=['POST'])
@login_required
def approveAccount(accid):
    print(accid)
    inputparam = request.get_json()
    print(inputparam)
    if request.method == 'POST':
        pending = AccountRequest.query.filter(AccountRequest.id==accid).first()
        if inputparam['approve'] == True:          
            pending.grant()
        else:
            pending.reject()
    return jsonify({'data':1})
