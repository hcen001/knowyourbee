from app.models import Base, PersonBase
from app import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Define a User model
class User(PersonBase):

    __tablename__ = 'user_account'

    # Identification Data: email & password
    password         = db.Column(db.String(192),  nullable=False)
    authenticated    = db.Column(db.Boolean, nullable=False, server_default='f', default=False)

    roles            = db.relationship('Role', secondary='user_role')

    # New instance instantiation procedure
    def __init__(self, email, password, fname, lname):
        self.email              = email
        self.password           = generate_password_hash(password)
        self.fname              = fname
        self.lname              = lname
        self.authenticated      = False

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

    def is_admin(self):
        for role in self.roles:
            if role.is_admin_role():
                return True
        return False

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
        return '<User: email={}, name={}>'.format(self.email, self.full_name)

class AccountRequest(PersonBase):

    __tablename__ = 'account_request'

    password         = db.Column(db.String(192), nullable=False)
    granted          = db.Column(db.Boolean, nullable=False, default=False, server_default='f')

    def __init__(self, email, password, fname, lname):

        self.email    = email
        self.password = generate_password_hash(password)
        self.fname    = fname
        self.lname    = lname
        self.granted  = False

    def request(self):
        db.session.add(self)
        db.session.commit()

    def grant(self):
        self.granted = True
        db.session.add(self)
        db.session.commit()

    @classmethod
    def accreqs_datatable(cls):
        data = cls.query.filter(AccountRequest.active == True)
        accreqs = []
        for accreq in data:
            _accreq = {}
            _accreq['id'] = accreq.id
            _accreq['fname'] = accreq.fname
            _accreq['lname'] = accreq.lname
            _accreq['email'] = accreq.email
            _accreq['phone'] = accreq.phone
            _accreq['password'] = accreq.password
            _accreq['granted'] = accreq.granted
            accreqs.append(_accreq)
        return accreqs

    def __repr__(self):
        return '<Account request: email={}, name={}>'.format(self.email, self.full_name())

class Role(Base):

    __tablename__ = 'role'

    name            = db.Column(db.String(64), nullable=False, default='Role', server_default='Role')
    description     = db.Column(db.String(256), default='A description', server_default='A description')
    can_admin       = db.Column(db.Boolean, nullable=False, default=False, server_default='f')

    users           = db.relationship('User', secondary='user_role')

    def __init__(self, name, description, can_admin=False):

        self.name           = name
        self.description    = description
        self.can_admin      = can_admin

    def __repr__(self):
        return '<Role: name={}>'.format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_admin_role(self):
        return self.can_admin

class UserRole(Base):

    __tablename__ = 'user_role'

    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    user = db.relationship('User', backref=db.backref('role'))
    role = db.relationship('Role', backref=db.backref('user'))

    def __init__(self, user_id, role_id):

        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return '<UserRole: email={}, role={}>'.format(self.user.email, self.role.name)
