from flask import Blueprint, request, render_template, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user

from app import db
from app.mod_auth.models import User
from app.mod_sample.models import Sample
from app.mod_specimen.models import Specimen
from app.mod_package.models import Package, Partner
from app.mod_package.forms import PackageForm
from app.mod_sample.forms import SampleForm
from app.mod_specimen.forms import SpecimenForm
from app.mod_util.utils import is_safe_url, parse_multi_form, parse_l
from app.mod_util.models import State, City

from datetime import datetime
from sqlalchemy.exc import IntegrityError

import json
import pprint

# Define the blueprint
mod_package = Blueprint('package', __name__)

@mod_package.route('/', methods=['GET'])
@login_required
def index():
    js = render_template('package/index.js')
    return render_template('package/index.html', user=current_user, title='Packages', js=js)

@mod_package.route('/all', methods=['GET'])
@login_required
def packages():
    data = Package.packages_datatable()
    output = {'data': data}
    return jsonify(output)

@mod_package.route('/<id>/details', methods=['GET'])
@login_required
def details(id):
    package_data = Package.query.get(id)
    js = render_template('package/details.js', package_id=package_data.id)
    return render_template('package/details.html', title='Details for package with ID {}'.format(package_data.id), user=current_user, package=package_data, js=js)

@mod_package.route('/country/<id>/states', methods=['GET'])
@login_required
def states(id):
    return jsonify(State.select_list(id))

@mod_package.route('/state/<id>/cities', methods=['GET'])
@login_required
def cities(id):
    return jsonify(City.select_list(id))

@mod_package.route('/add', methods=['GET', 'POST'])
@login_required
def add():

    if request.method == 'POST':
        data = parse_multi_form(request.form)
        # pp = pprint.PrettyPrinter(indent=4)

        data['package_id'] = str(data['package_id']).upper()
        data['date_sent'] = datetime.strptime(data['date_sent'],'%d/%B/%Y') if data['date_sent'] is not '' else None
        data['date_received'] = datetime.strptime(data['date_received'],'%d/%B/%Y') if data['date_received'] is not '' else None

        data = {k: None if v is '' else v for k, v in data.items()}
        # pp.pprint(data)
        # samples = data['samples']
        # for _, sample in samples.items():
        #     sample['sample_date_sampled'] = datetime.strptime(sample['sample_date_sampled'],'%d/%B/%Y')
        #     sample['sample_date_received'] = datetime.strptime(sample['sample_date_received'],'%d/%B/%Y')
        #     sample['latitude'] = parse_l(sample['latitude'])
        #     sample['longitude'] = parse_l(sample['longitude'])
        #     pp.pprint(sample)
        #     for _, specimen in sample['specimens'].items():
        #         if specimen['date_collected']:
        #             specimen['date_collected'] = datetime.strptime(specimen['date_collected'],'%d/%B/%Y')
        #         else:
        #             specimen['date_collected'] = None
        #         pp.pprint(specimen)

        package = Package(**data)

        try:
            package.add_or_update()
            samples = data['samples']
            for _, sample in samples.items():
                sample['package_id'] = package.id
                sample['sample_date_sampled'] = datetime.strptime(sample['sample_date_sampled'],'%d/%B/%Y')
                sample['sample_date_received'] = datetime.strptime(sample['sample_date_received'],'%d/%B/%Y')
                sample['latitude'] = parse_l(sample['latitude'])
                sample['longitude'] = parse_l(sample['longitude'])
                sample_db = Sample(**sample)
                sample_db.add_or_update()
                package.samples.append(sample_db)
                for _, specimen in sample['specimens'].items():
                    specimen['sample_id'] = sample_db.id
                    if specimen['date_collected']:
                        specimen['date_collected'] = datetime.strptime(specimen['date_collected'],'%d/%B/%Y')
                    else:
                        specimen['date_collected'] = None
                    specimen_db = Specimen(**specimen)
                    specimen_db.add_or_update()
                    sample_db.specimens.append(specimen_db)
        except IntegrityError as e:
            flash('Package with ID {} is already registered in the database.'.format(package.package_id), 'danger')
            return redirect(url_for('package.index'))
        else:
            package.save()

        flash('The package with ID {} was registered successfully.'.format(package.package_id), 'success')
        return redirect(url_for('package.index'))

    sample_form = SampleForm(formdata=None)
    specimen_form = SpecimenForm(formdata=None)
    package_form = PackageForm(formdata=None)
    js = render_template('package/add.js')
    return render_template('package/add.html', user=current_user, title='Add a new package', js=js, form=package_form, sample_form=sample_form, specimen_form=specimen_form)

@mod_package.route('/details/<id>/all_specimens', methods=['GET'])
@login_required
def specimens(id):
    data = Package.specimens_datatable(id)
    output = {'data': data}
    return jsonify(output)

@mod_package.route('/<id>/add_vials', methods=['GET', 'POST'])
@login_required
def add_vials(id):

    package = Package.query.filter(Package.id == id).first()

    if request.method == 'POST':
        data = parse_multi_form(request.form)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)

        try:
            samples = data['samples']
            for _, sample in samples.items():
                sample['package_id'] = package.id
                sample['sample_date_sampled'] = datetime.strptime(sample['sample_date_sampled'],'%d/%B/%Y')
                sample['sample_date_received'] = datetime.strptime(sample['sample_date_received'],'%d/%B/%Y')
                sample['latitude'] = parse_l(sample['latitude'])
                sample['longitude'] = parse_l(sample['longitude'])
                sample_db = Sample(**sample)
                sample_db.add_or_update()
                package.samples.append(sample_db)
                for _, specimen in sample['specimens'].items():
                    specimen['sample_id'] = sample_db.id
                    if specimen['date_collected']:
                        specimen['date_collected'] = datetime.strptime(specimen['date_collected'],'%d/%B/%Y')
                    else:
                        specimen['date_collected'] = None
                    specimen_db = Specimen(**specimen)
                    specimen_db.add_or_update()
                    sample_db.specimens.append(specimen_db)
        except Exception as e:
            flash('An error occured while trying to update package with ID {}.'.format(package.package_id), 'danger')
            return redirect(url_for('package.details', id=package.id))
        else:
            sample_db.save()

        flash('The package with ID {} was updated successfully.'.format(package.package_id), 'success')
        return redirect(url_for('package.details', id=package.id))


    sample_form = SampleForm()
    specimen_form = SpecimenForm()
    js = render_template('package/add_vials.js')
    return render_template('package/add_vials.html', user=current_user, title='Add a new vials to package', package=package, js=js, sample_form=sample_form, specimen_form=specimen_form)

@mod_package.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):

    if request.method == "GET":
        package_data = Package.query.get(id)
        form_data = {}
        form_data['package_id'] = package_data.package_id
        form_data['date_sent'] = package_data.date_sent
        form_data['date_received'] = package_data.date_received
        form_data['courier_id'] = package_data.courier_id
        form_data['tracking_number'] = package_data.tracking_number
        form_data['partner_id'] = package_data.partner_id or None
        form_data['location_id'] = package_data.location_id
        form_data['sender_id'] = package_data.sender_id
        form_data['receiver_id'] = package_data.receiver_id
        form_data['comments'] = package_data.comments
        form = PackageForm(data = form_data)

    if request.method == "POST":

        package_data = Package.query.filter(Package.id == id)
        old_package_id = package_data.first().package_id

        data = request.form.to_dict()
        data['package_id'] = str(data['package_id']).upper()
        data['date_sent'] = datetime.strptime(data['date_sent'],'%d/%B/%Y') if data['date_sent'] is not '' else None
        data['date_received'] = datetime.strptime(data['date_received'],'%d/%B/%Y') if data['date_received'] is not '' else None

        data = {k: None if v is '' else v for k, v in data.items()}

        try:
            package_data.update(data)
        except Exception as e:
            flash('There was an unexpected error when trying to update package with ID {}.'.format(e), 'danger')
        else:
            db.session.commit()
            flash('The package with ID {} was updated successfully.'.format(old_package_id), 'success')

        return redirect(url_for('package.details', id=id))


    js = render_template('package/edit.js')
    return render_template('package/edit.html', title='Edit information for package with ID {}'.format(package_data.id), form=form, user=current_user, package=package_data, js=js)
