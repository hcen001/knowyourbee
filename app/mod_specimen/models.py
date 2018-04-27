from app.models import Base
from app.mod_sample.models import Sample
from app import db

from app.mod_util.utils import GUID
import uuid

from sqlalchemy.dialects.postgresql import ENUM

db.GUID = GUID

genders = ('male', 'female')
castes = ('drone', 'worker', 'queen')
stages = ('egg', 'pupae', 'larvae', 'nymph', 'adult')

class Specimen(Base):

    __tablename__ = 'specimen'

    specimen_id         = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)
    gender              = db.Column(ENUM(*genders, name='gender_enum'), nullable=False)
    caste               = db.Column(ENUM(*castes, name='caste_enum'), nullable=False)
    development_stage   = db.Column(ENUM(*stages, name='dev_stage_enum'), nullable=False)
    sample_id           = db.Column(db.Integer, db.ForeignKey('sample.id'), nullable=False)

    genus_id            = db.Column(db.Integer, db.ForeignKey('genus.id'), nullable=False)
    species_id          = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)
    subspecies_id       = db.Column(db.Integer, db.ForeignKey('subspecies.id'), nullable=False)
    lineage_id          = db.Column(db.Integer, db.ForeignKey('lineage.id'), nullable=False)

    sample              = db.relationship('Sample', backref='_specimens', foreign_keys=[sample_id], lazy=True)
    genus               = db.relationship('Genus', backref='_specimens', foreign_keys=[genus_id], lazy=True)
    species             = db.relationship('Species', backref='_specimens', foreign_keys=[species_id], lazy=True)
    subspecies          = db.relationship('Subspecies', backref='_specimens', foreign_keys=[subspecies_id], lazy=True)
    lineage             = db.relationship('Lineage', backref='_specimens', foreign_keys=[lineage_id], lazy=True)

    def __init__(self, arg):

        self.arg = arg

class Genus(Base):

    __tablename__ = 'genus'

    genus_id            = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)
    name                = db.Column(db.String(128), nullable=False)

    def __init__(self, genus_id, name):

        self.genus_id = genus_id
        self.name = name

    def specimens(self):
        return self._specimens

    def __repr__(self):
        return '<Genus: ID={}, name={}>'.format(self.genus_id, self.name)

class Species(Base):

    __tablename__ = 'species'

    name                = db.Column(db.String(128), nullable=False)
    species_id          = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)

    def __init__(self, species_id, name):

        self.species_id = species_id
        self.name = name

    def specimens(self):
        return self._specimens

    def __repr__(self):
        return '<Species: ID={}, name={}>'.format(self.species_id, self.name)

class Subspecies(Base):

    __tablename__ = 'subspecies'

    name                = db.Column(db.String(128), nullable=False)
    subspecies_id       = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)

    def __init__(self, name, subspecies_id):

        self.name = name
        self.subspecies_id = subspecies_id

    def specimens(self):
        return self._specimens

    def __repr__(self):
        return '<Subspecies: ID={}, name={}>'.format(self.subspecies_id, self.name)

class Lineage(Base):

    __tablename__ = 'lineage'

    name                = db.Column(db.String(128), nullable=False)
    lineage_id          = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)

    def __init__(self, name, lineage_id):

        self.name = name
        self.lineage_id = lineage_id

    def specimens(self):
        return self._specimens

    def __repr__(self):
        return '<Subspecies: ID={}, name={}>'.format(self.lineage_id, self.name)
