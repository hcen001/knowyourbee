from flask import Blueprint, request, render_template, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user

from app.mod_auth.models import AccountRequest

import json


# Define the blueprint
mod_config = Blueprint('config', __name__)

@mod_config.route('/accreq/', methods=['GET'])
@login_required
def accreqIndex():
    js = render_template('config/accreq/index.js')
    return render_template('config/accreq/index.html', user=current_user, title='Account Request', js=js)

@mod_config.route('/accreq/all', methods=['GET'])
@login_required
def accreqs():
    data = AccountRequest.accreqs_datatable()
    output = {'data': data}
    return jsonify(output)

@mod_config.route('/accreq/approveAccount/<accid>', methods=['POST'])
@login_required
def approveAccount(accid):
    print(accid)
    inputparam = request.get_json()
    print(inputparam)
    if request.method == 'POST':
        pending = AccountRequest.query.filter(AccountRequest.id==accid).first()
        if inputparam['approve'] == True:          
            pending.grant(True)
        else:
            pending.grant(False)
    return jsonify({'data':1})
