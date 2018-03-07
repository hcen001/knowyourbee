from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_dashboard.controllers import entry_point as entry_point

# Register blueprint(s)
app.register_blueprint(entry_point)
app.register_blueprint(auth_module)

# Load Boostrap
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

# from app import routes
