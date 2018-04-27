from app.models import Base, PersonBase
from app import db

from app.mod_util.utils import GUID
import uuid

db.GUID = GUID

class Package(Base):

    __tablename__       = 'package'

    package_id          = db.Column('package_id', db.GUID(), default=uuid.uuid4(), nullable=False)
    date_sent           = db.Column('date_sent', db.DateTime, default=db.func.current_timestamp(), nullable=False)
    date_received       = db.Column('date_received', db.DateTime, default=db.func.current_timestamp(), nullable=True)
    tracking_number     = db.Column('tracking_number', db.String(64))
    sender_source_id    = db.Column('sender_source_id', db.String(64), nullable=True)
    comments            = db.Column('comments', db.String(512), nullable=True)

    partner_id          = db.Column('partner_id', db.Integer, db.ForeignKey('partner.id'), nullable=False)
    location_id         = db.Column('location_id', db.Integer, db.ForeignKey('location.id'), nullable=False)
    courier_id          = db.Column('courier_id', db.Integer, db.ForeignKey('courier.id'), nullable=False)
    sender_id           = db.Column('sender_id', db.Integer, db.ForeignKey('person.id'), nullable=False)
    receiver_id         = db.Column('receiver_id', db.Integer, db.ForeignKey('person.id'), nullable=False)

    partner             = db.relationship('Partner', backref='_packages', foreign_keys=[partner_id], lazy=True)
    location            = db.relationship('Location', backref='_packages', foreign_keys=[location_id], lazy=True)
    courier             = db.relationship('Courier', backref='_packages', foreign_keys=[courier_id], lazy=True)
    sender              = db.relationship('Person', backref='_sent_packages', foreign_keys=[sender_id], lazy=True)
    receiver            = db.relationship('Person', backref='_received_packages', foreign_keys=[receiver_id], lazy=True)

    def __init__(self, date_sent, date_received, tracking_number, partner_id, location_id,
                courier_id, sender_id, receiver_id, sender_source_id, comments=''):

        self.date_sent = date_sent
        self.date_received = date_received
        self.tracking_number = tracking_number
        self.sender_source_id = sender_source_id
        self.comments = comments

        self.partner_id = partner_id
        self.location_id = location_id
        self.courier_id = courier_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id

    def stored_at(self):
        return self.location

    def sent_by(self):
        return self.sender

    def received_by(self):
        return self.receiver

    def partner(self):
        return self.partner

    def partner_institution(self):
        return self.partner().institution

    def partner_contact(self):
        return self.partner().email

    def partner_phone(self):
        return self.partner().phone

    def samples(self):
        #backref from mod_sample: Sample
        return self._samples

class Person(PersonBase):

    __tablename__ = 'person'

    def __init__(self, fname, lname, email, phone):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone

    def sent_packages(self):
        return self._sent_packages

    def received_packages(self):
        return self._received_packages

    def processed_samples(self):
        return self._processed_samples

    def collected_samples(self):
        return self._collected_samples

    def __repr__(self):
        return '<Person: name={}, email={}, phone={}>'.format(self.name, self.email, self.phone)

class Partner(PersonBase):

    __tablename__    = 'partner'

    institution      = db.Column(db.String(256))

    def __init__(self, fname, lname, email, institution, phone):
        self.fname          = fname
        self.lname          = lname
        self.email          = email
        self.institution    = institution
        self.phone          = phone

    def packages(self):
        return self._packages

    def __repr__(self):
        return '<Partner: name={}, email={}, institution={}, phone={}>'.format(self.full_name, self.email, self.institution, self.phone)

class Location(Base):

    __tablename__ = 'location'

    name            = db.Column(db.String(256), nullable=False)
    description     = db.Column(db.String(512), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def packages(self):
        return self._packages

    def processed_samples(self):
        return self._samples

    def __repr__(self):
        return '<Location: name={}>'.format(self.name)

class Courier(Base):

    __tablename__   = 'courier'

    name            = db.Column(db.String(64), nullable=False)
    description     = db.Column(db.String(128), nullable=False)

    def __init__(self, name, description):

        self.name = name
        self.description = description

    def packages(self):
        return self._packages

    def __repr__(self):
        return '<Courier: name={}>'.format(self.name)
