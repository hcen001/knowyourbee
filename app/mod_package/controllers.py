from flask import Blueprint, request, render_template, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user

from app import login
from app.mod_auth.models import User
from app.mod_sample.models import Sample
from app.mod_specimen.models import Specimen
from app.mod_package.models import Package, Partner
from app.mod_package.forms import PackageForm
from app.mod_sample.forms import SampleForm
from app.mod_specimen.forms import SpecimenForm
from app.mod_util.utils import is_safe_url, parse_multi_form, package_id_gen
from app.mod_util.models import State, City

from datetime import datetime

import json

## commenting this exception helps debugging when there are issues with importing
@login.user_loader
def load_user(id):
    try:
        return User.query.filter(User.id == int(id)).first()
    except User.DoesNotExist:
        return None

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

@mod_package.route('/details/<id>', methods=['GET'])
@login_required
def details(id):
    package_data = Package.query.get(id)
    js = render_template('package/details.js')
    return render_template('package/details.html', user=current_user, title='Details for package with ID {}'.format(package_data.package_id), package=package_data, js=js)

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
        # package_form = PackageForm(request.form)
        # if package_form.validate_on_submit():
            # print('Validated')
        data = parse_multi_form(request.form)
        print('data before pre processing: ', data)
        country = data.get('pack_country') or None
        state = data.get('pack_state') or None
        print('state: ', state)
        data['package_id'] = package_id_gen(country, state)
        data['date_sent'] = datetime.strptime(data['date_sent'],'%d/%m/%Y')
        data['date_received'] = datetime.strptime(data['date_received'],'%d/%m/%Y')
        print('data after pre processing: ', data)
        # package = Package(**data)
        # package.add_or_update()
        # samples = data['samples']
        # for _, sample in samples.items():
        #     sample['package_id'] = package.id
        #     sample['sample_date_sampled'] = datetime.strptime(sample['sample_date_sampled'],'%d/%m/%Y')
        #     sample['sample_date_received'] = datetime.strptime(sample['sample_date_received'],'%d/%m/%Y')
        #     sample['coordinates'] = None
        #     sample_db = Sample(**sample)
        #     sample_db.add_or_update()
        #     for _, specimen in sample['specimens'].items():
        #         specimen['sample_id'] = sample_db.id
        #         specimen['sample_quality'] = True if specimen['sample_quality'] == 1 else False
        #         specimen_db = Specimen(**specimen)
        #         specimen_db.add_or_update()

        return redirect(url_for('package.index'))
        # else:
            # print('Not validated')

    package_form = PackageForm()
    sample_form = SampleForm()
    specimen_form = SpecimenForm()
    js = render_template('package/add.js')
    package_form = PackageForm(request.form)
    return render_template('package/add.html', user=current_user, title='Add a new package', js=js, form=package_form, sample_form=sample_form, specimen_form=specimen_form)
