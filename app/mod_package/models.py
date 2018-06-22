from app.models import Base, PersonBase
from app import db

from sqlalchemy.dialects.postgresql import ARRAY, Any

import json

class Package(Base):

    __tablename__       = 'package'

    package_id          = db.Column('package_id', db.String(64), default='SOUTH AFRICA', unique=True, nullable=False)
    date_sent           = db.Column('date_sent', db.DateTime, default=db.func.current_timestamp(), nullable=False)
    date_received       = db.Column('date_received', db.DateTime, default=db.func.current_timestamp(), nullable=True)
    tracking_number     = db.Column('tracking_number', db.String(64))
    # sender_source_id    = db.Column('sender_source_id', db.String(64), nullable=True)
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

    samples             = db.relationship('Sample', back_populates='package')

    def __init__(self, **kwargs):

        self.package_id = kwargs.get('package_id')
        self.date_sent = kwargs.get('date_sent')
        self.date_received = kwargs.get('date_received')
        self.tracking_number = kwargs.get('tracking_number') or None
        self.comments = kwargs.get('comments') or None

        self.partner_id = kwargs.get('partner_id')
        self.location_id = kwargs.get('location_id')
        self.courier_id = kwargs.get('courier_id')
        self.sender_id = kwargs.get('sender_id')
        self.receiver_id = kwargs.get('receiver_id')

    def stored_at(self):
        return self.location

    def sent_by(self):
        return self.sender

    def received_by(self):
        return self.receiver

    def vials(self):
        return len(self.samples)

    @classmethod
    def packages_datatable(cls):
        data = cls.query.filter(Package.active == True)
        packages = []
        for package in data:
            _package = {}
            _package['id'] = package.id
            _package['package_id'] = package.package_id
            _package['date_sent'] = package.date_sent.strftime('%d/%B/%Y')
            _package['date_received'] = package.date_received.strftime('%d/%B/%Y')
            _package['partner_name'] = package.partner.full_name
            _package['process_location'] = package.location.name
            _package['sender'] = package.sender.full_name
            _package['receiver'] = package.receiver.full_name
            packages.append(_package)
        return packages

    @classmethod
    def specimens_datatable(cls, id):
        # pass
        data = cls.query.filter(Package.active == True, Package.id == id)
        _specimens = []
        for package in data:
            vials = package.samples
            for vial in vials:
                specimens = vial.specimens
                number_specimen = 0
                for specimen in specimens:
                    _specimen = {}
                    number_specimen += 1
                    _specimen['collection_sample_id'] = specimen.collection_sample_id
                    _specimen['cooperator'] = specimen.sample.collected_by().full_name
                    _specimen['number_specimens'] = '{}/{}'.format(number_specimen, len(specimens))
                    _specimen['date_received'] = specimen.sample.date_received.strftime('%d/%B/%Y')
                    _specimen['country'] = specimen.sample.country.name
                    # _specimen['state'] = specimen.sample.origin_state or 'N/A'
                    _specimen['latitude'] = specimen.sample.latitude or 'N/A'
                    _specimen['longitude'] = specimen.sample.longitude or 'N/A'
                    _specimen['genus'] = specimen.sample.genus.name
                    _specimen['species'] = specimen.sample.species.name
                    _specimen['subspecies'] = specimen.sample.subspecies.name
                    _specimen['lineage'] = specimen.sample.lineage.name
                    _specimen['gender'] = specimen.sample.gender
                    _specimen['freezer'] = specimen.sample.freezer or 'N/A'
                    _specimen['box'] = specimen.sample.box or 'N/A'
                    _specimen['dna'] = specimen.dna or 'N/A'
                    _specimen['body_part'] = specimen.body_part or 'N/A'
                    _specimen['dna_freezer'] = specimen.freezer or 'N/A'
                    _specimen['dna_box'] = specimen.box or 'N/A'
                    _specimen['comments'] = specimen.comments or 'None'
                    _specimens.append(_specimen)
        return _specimens

    def __repr__(self):
        return '<Package: ID={}, sent={}, received={}, partner={}>'.format(self.package_id, self.date_sent, self.date_received, self.partner)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Person(PersonBase):

    __tablename__ = 'person'

    role            = db.Column(ARRAY(db.String(4)), default='{P}', server_default='{P}', nullable=False)

    def __init__(self, **kwargs):

        self.fname = kwargs.get('first_name')
        self.lname = kwargs.get('last_name')
        self.email = kwargs.get('email')
        self.phone = kwargs.get('phone')
        self.role = kwargs.get('role')

    def sent_packages(self):
        return self._sent_packages

    def received_packages(self):
        return self._received_packages

    def processed_samples(self):
        return self._processed_samples

    def collected_samples(self):
        return self._collected_samples

    @classmethod
    def select_list(cls, roles):
        persons = cls.query.filter(cls.active == True, cls.role.contains(roles)).all()
        data = [(person.id, person.full_name) for person in persons]
        data.insert(0,('',''))
        return data

    @classmethod
    def collaborators(cls):
        _persons = cls.query.filter(cls.active == True)

        persons = []

        for person in _persons:
            _person = {}
            _person['id'] = person.id
            _person['name'] = person.full_name
            _person['email'] = person.email
            _person['phone'] = person.phone
            _person['role'] = person.role
            _person['active'] = person.active
            persons.append(_person)

        return persons


    def __repr__(self):
        return '<Person: name={}, email={}, phone={}>'.format(self.full_name, self.email, self.phone)

class Partner(PersonBase):

    __tablename__    = 'partner'

    institution      = db.Column(db.String(256))

    def __init__(self, fname, lname, email, institution, phone):
        self.fname          = fname
        self.lname          = lname
        self.email          = email
        self.institution    = institution
        self.phone          = phone

    @classmethod
    def select_list(cls):
        partners = cls.query.filter(cls.active == True)
        data = [(partner.id, partner.full_name+' - '+partner.institution) for partner in partners]
        data.insert(0,('',''))
        return data

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

    @classmethod
    def select_list(cls):
        locations = cls.query.filter(cls.active == True)
        data = [(location.id, location.name) for location in locations]
        data.insert(0,('',''))
        return data

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

    @classmethod
    def select_list(cls):
        couriers = cls.query.filter(cls.active == True)
        data = [(courier.id, courier.name) for courier in couriers]
        data.insert(0,('',''))
        return data

    def __repr__(self):
        return '<Courier: name={}>'.format(self.name)
