from app.models import Base, PersonBase
from app import db

class Package(Base):

    __tablename__       = 'package'

    package_id          = db.Column(db.String(128), nullable=False)
    date_sent           = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    date_received       = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    tracking_number     = db.Column(db.String(64))
    comments            = db.Column(db.String(512))

    partner_id          = db.Column(db.Integer, db.ForeignKey('partner.id'), nullable=False)
    location_id         = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    courier_id          = db.Column(db.Integer, db.ForeignKey('courier.id'), nullable=False)
    sender_id           = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    receiver_id         = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

    partner             = db.relationship('Partner', backref='packages', lazy=True)
    location            = db.relationship('Location', backref='packages', lazy=True)
    courier             = db.relationship('Courier', backref='packages', lazy=True)
    sender              = db.relationship('Person', backref='sent_packages', lazy=True)
    receiver            = db.relationship('Person', backref='received_packages', lazy=True)

    def __init__(self, arg):
        self.arg = arg

    def stored_at(self):
        return self.location.name

    def sent_by(self):
        return self.sender.name

    def received_by(self):
        return self.receiver.name

    def partner_name(self):
        return self.partner.name

    def partner_institution(self):
        return self.partner.institution

class Person(PersonBase):

    __tablename__ = 'person'

    def __init__(self, fname, lname, email, phone):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone

    def __repr__():
        return '<Person: name={}, email={}, phone={}>'.format(self.name, self.email)

class Partner(PersonBase):

    __tablename__    = 'partner'

    institution      = db.Column(db.String(256))

    def __init__(self, fname, lname, email, institution, phone):
        self.fname          = fname
        self.lname          = lname
        self.email          = email
        self.institution    = institution
        self.phone          = phone

    def __repr__(self):
        return '<Partner: name={}, email={}, institution={}, phone={}>'.format(self.name, self.email, self.institution, self.phone)

class Location(Base):

    __tablename__ = 'location'

    name            = db.Column(db.Column(db.String(256)), nullable=False)
    description     = db.Column(db.Column(db.String(512)), nullable=False)

    packages        = db.relationship('Package', backref='packages', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__():
        return '<Location: name={}>'.format(self.name)

class Courier(Base):

    __tablename__   = 'courier'

    name            = db.Column(db.Column(db.String(64)), nullable=False)
    description     = db.Column(db.Column(db.String(128)), nullable=False)

    packages        = db.relationship('Package', backref='packages', lazy=True)

    def __init__(self, name, description):

        self.name = name
        self.description = description

    def __repr__():
        return '<Courier: name={}>'.format(self.name)
