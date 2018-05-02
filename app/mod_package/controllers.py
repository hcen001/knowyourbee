from flask import Blueprint, request, render_template, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user

from app import login
from app.mod_auth.models import User
from app.mod_package.models import Package, Partner
from app.mod_package.forms import PackageForm
from app.mod_util.utils import is_safe_url

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

@mod_package.route('/add', methods=['GET', 'POST'])
@login_required
def add():

    package_form = PackageForm()
    if request.method == 'POST':
        package_form = PackageForm(request.form)
        if package_form.validate_on_submit():
            pass
        pass
    js = render_template('package/add.js')

    return render_template('package/add.html', user=current_user, title='Add a new package', js=js, form=package_form)