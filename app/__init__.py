from flask import Flask

app = Flask(__name__, instance_relative_config=True, static_folder='static')

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

# Load database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Load Login manager
from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'auth.login'

# Register blueprint(s)
from app.mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module, url_prefix='/auth')

from app.mod_dashboard.controllers import entry_point
app.register_blueprint(entry_point)

from app.mod_package.controllers import mod_package
app.register_blueprint(mod_package, url_prefix='/packages')

from app.mod_sample.controllers import mod_sample
app.register_blueprint(mod_sample, url_prefix='/samples')

from app.mod_specimen.controllers import mod_specimen
app.register_blueprint(mod_specimen, url_prefix='/specimens')

from app.mod_accreq.controllers import mod_accreq
app.register_blueprint(mod_accreq, url_prefix='/accreq')

from app.mod_util.models import Country, State, City

#
@app.shell_context_processor
def make_shell_context():
    from app.mod_auth.models import User, Role, UserRole
    from app.mod_package.models import Package, Person, Partner, Location, Courier
    from app.mod_sample.models import Sample
    from app.mod_specimen.models import Specimen, Genus, Species, Subspecies, Lineage
    from app.mod_util.models import Country, State, City

    return {'db': db, 'User': User, 'Role': Role, 'UserRole': UserRole, 'Package': Package, \
            'Sample': Sample, 'Specimen': Specimen, 'Genus': Genus, 'Species': Species, 'Subspecies': Subspecies, 'Lineage': Lineage,  \
            'Person': Person, 'Partner': Partner, 'Location': Location, 'Courier': Courier, \
            'Country': Country, 'State': State, 'City': City}
