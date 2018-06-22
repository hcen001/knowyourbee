from flask import Blueprint, request, render_template, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user

from app.mod_auth.models import AccountRequest
from app.mod_config.forms import CollaboratorForm
from app.mod_package.models import Person
from app.mod_util.utils import parse_multi_form

import json
import pprint


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

@mod_config.route('/accreq/approveAccount', methods=['POST'])
@login_required
def approveAccount():

    if request.method == 'POST':
        inputparam = request.get_json()
        pending = AccountRequest.query.filter(AccountRequest.id==inputparam['accid']).first()
        if inputparam['approve'] is True:
            pending.grant()
        else:
            pending.grant(False)
    return jsonify({})

@mod_config.route('/collaborators/deactivate', methods=['GET'])
@mod_config.route('/collaborators/list', methods=['GET'])
@mod_config.route('/collaborators', methods=['GET', 'POST'])
@login_required
def admin_collaborators():

    print('********DEBUG*********', request.path)

    add_collaborator_form = CollaboratorForm()
    js = render_template('config/collaborators/index.js')

    if request.method == 'POST':
        _data = {}
        _data['first_name'] = request.form.get('first_name')
        _data['last_name'] = request.form.get('last_name')
        _data['email'] = request.form.get('email')
        _data['phone'] = request.form.get('phone')
        _data['role'] = request.form.getlist('roles')
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data)
        # pp.pprint(_data)
        try:
            p = Person(**_data)
            p.add_or_update()
        except Exception as e:
            flash('An unexpected error occurred while trying to add a new record to the database', 'danger')
            return redirect(url_for('package.index'))
        else:
            p.save()

        flash('Collaborator {} successfully added to the database.'.format(p.full_name), 'success')
        return render_template('config/collaborators/index.html', form=add_collaborator_form, user=current_user, title='Collaborators', js=js)

    endpoint = request.path.split('/')[-1]

    if endpoint == 'list':
        data = Person.collaborators()
        output = {'data': data}
        return jsonify(output)

    return render_template('config/collaborators/index.html', form=add_collaborator_form, user=current_user, title='Collaborators', js=js)

@mod_config.route('/institutions/add', methods=['POST'])
@mod_config.route('/institutions', methods=['GET'])
@login_required
def admin_institutions():
    pass

@mod_config.route('/partners/add', methods=['POST'])
@mod_config.route('/partners', methods=['GET'])
@login_required
def admin_partners():
    pass

@mod_config.route('/locations/add', methods=['POST'])
@mod_config.route('/locations', methods=['GET'])
@login_required
def admin_locations():
    pass

@mod_config.route('/couriers/add', methods=['POST'])
@mod_config.route('/couriers', methods=['GET'])
@login_required
def admin_couriers():
    pass