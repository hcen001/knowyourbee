from app.models import Base
from app import db

from werkzeug.security import generate_password_hash, check_password_hash

# Define a User model
class User(Base):

    __tablename__ = 'user'

    # Identification Data: email & password
    email            = db.Column(db.String(128),  nullable=False, unique=True)
    password         = db.Column(db.String(192),  nullable=False)
    authenticated    = db.Column(db.Boolean, nullable=False, server_default='f', default=False)
    fname            = db.Column(db.String(50),  nullable=False)
    lname            = db.Column(db.String(50),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, email, password, fname, lname):

        self.email    = email
        self.password = password
        self.fname    = fname
        self.lname    = lname
        self.is_authenticated = False

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def authenticate(self):
        self.authenticated = True
        db.session.add(self)
        db.session.commit()

    def logout(self):
        self.authenticated = False
        db.session.add(self)
        db.session.commit()

    def forgot_password(self):
        print(self)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def __repr__(self):
        return '<User: email={}, fname={}, lname={}>'.format(self.email, self.fname, self.lname)
