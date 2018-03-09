from flask import Flask

app = Flask(__name__, instance_relative_config=True)

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

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_dashboard.controllers import entry_point as entry_point

# Register blueprint(s)
app.register_blueprint(entry_point)
app.register_blueprint(auth_module)

# Load Boostrap
# from flask_bootstrap import Bootstrap
# bootstrap = Bootstrap(app)

#
@app.shell_context_processor
def make_shell_context():
    return {'db': db}

from app.mod_auth import models
