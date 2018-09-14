from flask import Blueprint, request, render_template, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user

from app.mod_auth.models import AccountRequest
from app.mod_config.forms import CollaboratorForm, PartnerForm, LocationForm, CourierForm
from app.mod_package.models import Person, Partner, Location, Courier
from app.mod_auth.models import User
from app.mod_auth.forms import NewUserForm
from app.mod_util.utils import parse_multi_form

from app import db

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

@mod_config.route('/collaborators/update_status', methods=['POST'])
@mod_config.route('/collaborators/update', methods=['POST'])
@mod_config.route('/collaborators/list', methods=['GET'])
@mod_config.route('/collaborators', methods=['GET', 'POST'])
@login_required
def admin_collaborators():

    add_collaborator_form = CollaboratorForm()
    js = render_template('config/collaborators/index.js')

    req_form = CollaboratorForm(request.form)

    endpoint = request.path.split('/')[-1]

    if request.method == 'POST' and req_form.validate():

        if endpoint == 'update':
            _data = {}
            _data['fname'] = request.form.get('first_name')
            _data['lname'] = request.form.get('last_name')
            _data['email'] = request.form.get('email')
            _data['phone'] = request.form.get('phone')
            _data['role'] = request.form.getlist('roles')
            collaborator_id = request.form.get('collaborator_id')
            collaborator_data = Person.query.filter(Person.id == collaborator_id)

            try:
                collaborator_data.update(_data)
            except Exception as e:
                flash('There was an unexpected error when trying to update collaborator with name {}.'.format(collaborator_data.first().full_name), 'danger')
            else:
                db.session.commit()

            flash('Collaborator {} successfully updated in the database.'.format(collaborator_data.first().full_name), 'success')
            return redirect(url_for('.admin_collaborators'))

        try:
            _data = {}
            _data['first_name'] = request.form.get('first_name')
            _data['last_name'] = request.form.get('last_name')
            _data['email'] = request.form.get('email')
            _data['phone'] = request.form.get('phone')
            _data['role'] = request.form.getlist('roles')
            p = Person(**_data)
            p.add_or_update()
        except Exception as e:
            flash('An unexpected error occurred while trying to add a new record to the database', 'danger')
            return redirect(url_for('config.admin_collaborators'))
        else:
            p.save()

        flash('Collaborator {} successfully added to the database.'.format(p.full_name), 'success')
        return render_template('config/collaborators/index.html', form=add_collaborator_form, user=current_user, title='Collaborators', js=js)

    if endpoint == 'list' and request.method == 'GET':
        data = Person.collaborators()
        output = {'data': data}
        return jsonify(output)

    if endpoint == 'update_status' and request.method == 'POST':

        data = request.get_json()

        action = data['action']
        collaborator_id = data['collaborator_id']

        if action == 'reactivate':
            p = Person.query.filter(Person.id==collaborator_id, Person.active==False).first()
            p.add_or_update(True)
            message = 'Collaborator {} successfully reactivated in the database.'.format(p.full_name)
        if action == 'deactivate':
            p = Person.query.filter(Person.id==collaborator_id, Person.active==True).first()
            p.add_or_update(False)
            message = 'Collaborator {} successfully deactivated in the database.'.format(p.full_name)

        p.save()
        flash(message, 'success')
        return jsonify({})

    return render_template('config/collaborators/index.html', form=add_collaborator_form, user=current_user, title='Collaborators', js=js)

@mod_config.route('/partners/update_status', methods=['POST'])
@mod_config.route('/partners/update', methods=['POST'])
@mod_config.route('/partners/list', methods=['GET'])
@mod_config.route('/partners', methods=['GET', 'POST'])
@login_required
def admin_partners():

    add_partner_form = PartnerForm()
    js = render_template('config/partners/index.js')
    req_form = PartnerForm(request.form)

    endpoint = request.path.split('/')[-1]

    if request.method == 'POST' and req_form.validate():

        if endpoint == 'update':
            _data = {}
            _data['fname'] = request.form.get('first_name')
            _data['lname'] = request.form.get('last_name')
            _data['email'] = request.form.get('email')
            _data['phone'] = request.form.get('phone')
            _data['institution'] = request.form.get('institution')
            partner_id = request.form.get('partner_id')
            partner_data = Partner.query.filter(Partner.id == partner_id)

            try:
                partner_data.update(_data)
            except Exception as e:
                flash('There was an unexpected error when trying to update partner with name {}.'.format(partner_data.first().full_name), 'danger')
            else:
                db.session.commit()

            flash('Partner {} successfully updated in the database.'.format(partner_data.first().full_name), 'success')
            return redirect(url_for('.admin_partners'))

        _data = {}
        _data['fname'] = request.form.get('first_name')
        _data['lname'] = request.form.get('last_name')
        _data['email'] = request.form.get('email')
        _data['phone'] = request.form.get('phone')
        _data['institution'] = request.form.get('institution')

        try:
            p = Partner(**_data)
            p.add_or_update()
        except Exception as e:
            flash('An unexpected error occurred while trying to add a new record to the database', 'danger')
            return redirect(url_for('.admin_partners'))
        else:
            p.save()

        flash('Partner {} successfully added to the database.'.format(p.full_name), 'success')
        return render_template('config/partners/index.html', form=add_partner_form, user=current_user, title='Partners', js=js)

    if endpoint == 'update_status' and request.method == 'POST':

        data = request.get_json()

        action = data['action']
        partner_id = data['partner_id']

        if action == 'reactivate':
            p = Partner.query.filter(Partner.id==partner_id, Partner.active==False).first()
            p.add_or_update(True)
            message = 'Partner {} successfully reactivated in the database.'.format(p.full_name)
        if action == 'deactivate':
            p = Partner.query.filter(Partner.id==partner_id, Partner.active==True).first()
            p.add_or_update(False)
            message = 'Partner {} successfully deactivated in the database.'.format(p.full_name)

        p.save()
        flash(message, 'success')
        return jsonify({})

    if endpoint == 'list' and request.method == 'GET':
        data = Partner.list()
        output = {'data': data}
        return jsonify(output)

    return render_template('config/partners/index.html', form=add_partner_form, user=current_user, title='Partners', js=js)

@mod_config.route('/locations/update_status', methods=['POST'])
@mod_config.route('/locations/update', methods=['POST'])
@mod_config.route('/locations/list', methods=['GET'])
@mod_config.route('/locations', methods=['GET', 'POST'])
@login_required
def admin_locations():

    add_location_form = LocationForm()
    js = render_template('config/locations/index.js')
    req_form = LocationForm(request.form)

    endpoint = request.path.split('/')[-1]

    if request.method == 'POST' and req_form.validate():

        if endpoint == 'update':
            _data = {}
            _data['name'] = request.form.get('name')
            _data['description'] = request.form.get('description')
            location_id = request.form.get('location_id')
            location_data = Location.query.filter(Location.id == location_id)

            try:
                location_data.update(_data)
            except Exception as e:
                flash('There was an unexpected error when trying to update the location with name {}.'.format(location_data.first().name), 'danger')
            else:
                db.session.commit()

            flash('Location {} successfully updated in the database.'.format(location_data.first().name), 'success')
            return redirect(url_for('.admin_locations'))

        _data = {}
        _data['name'] = request.form.get('name')
        _data['description'] = request.form.get('description')

        try:
            l = Location(**_data)
            l.add_or_update()
        except Exception as e:
            flash('An unexpected error occurred while trying to add a new record to the database', 'danger')
            return redirect(url_for('config.admin_locations'))
        else:
            l.save()

        flash('Location {} successfully added to the database.'.format(l.name), 'success')
        return render_template('config/locations/index.html', form=add_location_form, user=current_user, title='Locations', js=js)

    if endpoint == 'list' and request.method == 'GET':
        data = Location.list()
        output = {'data': data}
        return jsonify(output)

    if endpoint == 'update_status' and request.method == 'POST':

        data = request.get_json()

        action = data['action']
        location_id = data['location_id']

        if action == 'reactivate':
            l = Location.query.filter(Location.id==location_id, Location.active==False).first()
            l.add_or_update(True)
            message = 'Location {} successfully reactivated in the database.'.format(l.name)
        if action == 'deactivate':
            l = Location.query.filter(Location.id==location_id, Location.active==True).first()
            l.add_or_update(False)
            message = 'Location {} successfully deactivated in the database.'.format(l.name)

        l.save()
        flash(message, 'success')
        return jsonify({})

    return render_template('config/locations/index.html', form=add_location_form, user=current_user, title='Locations', js=js)

@mod_config.route('/couriers/update', methods=['POST'])
@mod_config.route('/couriers/update_status', methods=['POST'])
@mod_config.route('/couriers/list', methods=['GET'])
@mod_config.route('/couriers', methods=['GET', 'POST'])
@login_required
def admin_couriers():

    add_courier_form = CourierForm()
    js = render_template('config/couriers/index.js')
    req_form = CourierForm(request.form)

    endpoint = request.path.split('/')[-1]

    if request.method == 'POST' and req_form.validate():

        if endpoint == 'update':
            _data = {}
            _data['name'] = request.form.get('name')
            _data['description'] = request.form.get('description')
            courier_id = request.form.get('courier_id')
            courier_data = Courier.query.filter(Courier.id == courier_id)

            try:
                courier_data.update(_data)
            except Exception as e:
                flash('There was an unexpected error when trying to update the courier with name {}.'.format(courier_data.first().name), 'danger')
            else:
                db.session.commit()

            flash('Courier {} successfully updated in the database.'.format(courier_data.first().name), 'success')
            return redirect(url_for('.admin_couriers'))

        _data = {}
        _data['name'] = request.form.get('name')
        _data['description'] = request.form.get('description')
        try:
            c = Courier(**_data)
            c.add_or_update()
        except Exception as e:
            flash('An unexpected error occurred while trying to add a new record to the database', 'danger')
            return redirect(url_for('config.admin_couriers'))
        else:
            c.save()

        flash('Courier {} successfully added to the database.'.format(c.name), 'success')
        return render_template('config/couriers/index.html', form=add_courier_form, user=current_user, title='Couriers', js=js)

    if endpoint == 'list' and request.method == 'GET':
        data = Courier.list()
        output = {'data': data}
        return jsonify(output)

    if endpoint == 'update_status' and request.method == 'POST':

        data = request.get_json()

        action = data['action']
        courier_id = data['courier_id']

        if action == 'reactivate':
            c = Courier.query.filter(Courier.id==courier_id, courier.active==False).first()
            c.add_or_update(True)
            message = 'Courier {} successfully reactivated in the database.'.format(c.name)
        if action == 'deactivate':
            c = Courier.query.filter(Courier.id==courier_id, courier.active==True).first()
            c.add_or_update(False)
            message = 'Courier {} successfully deactivated in the database.'.format(c.name)

        l.save()
        flash(message, 'success')
        return jsonify({})

    return render_template('config/couriers/index.html', form=add_courier_form, user=current_user, title='Couriers', js=js)

@mod_config.route('/users/update_status', methods=['POST'])
@mod_config.route('/users/list', methods=['GET'])
@mod_config.route('/users', methods=['GET', 'POST'])
@login_required
def admin_users():

    add_user_form = NewUserForm()
    js = render_template('config/users/index.js')

    endpoint = request.path.split('/')[-1]

    if endpoint == 'list' and request.method == 'GET':
        data = User.list()
        output = {'data': data}
        return jsonify(output)

    if endpoint == 'update_status' and request.method == 'POST':

        data = request.get_json()

        action = data['action']
        user_id = data['user_id']

        if action == 'reactivate':
            u = User.query.filter(User.id==user_id, User.active==False).first()
            u.add_or_update(True)
            message = 'User {} successfully reactivated in the database.'.format(u.full_name)

        if action == 'deactivate':
            u = User.query.filter(User.id==user_id, User.active==True).first()
            u.authenticated = False
            u.add_or_update(False)
            message = 'User {} successfully deactivated in the database.'.format(u.full_name)

        if action == 'logout':
            u = User.query.filter(User.id==user_id, User.active==True).first()
            if current_user != u and u is not None:
                u.add_or_update(False)
                message = 'User {} successfully deactivated in the database.'.format(u.full_name)
            else:
                message = 'You cannot use this panel to logout yourself. Please, use the logout option to exit the application.'

        u.save()
        flash(message, 'success')
        return jsonify({})

    return render_template('config/users/index.html', form=add_user_form, user=current_user, title='Users', js=js)
