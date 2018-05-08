from app.models import Base, TaxonBase
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

    specimen_id         = db.Column(db.GUID(), default=uuid.uuid1(), nullable=False)
    collection_sample_id    = db.Column(db.String(32), nullable=False, default='122', server_default='122')
    sample_quality      = db.Column(db.Boolean, default=True, server_default='t', nullable=False)
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

    def __init__(self, **kwargs):

        self.sample_id = kwargs.get('sample_id')
        self.collection_sample_id = kwargs.get('collection_sample_id')
        self.gender = kwargs.get('gender')
        self.caste = kwargs.get('caste')
        self.development_stage = kwargs.get('stage')
        self.genus_id = kwargs.get('genus_id')
        self.species_id = kwargs.get('species_id')
        self.subspecies_id = kwargs.get('subspecies_id')
        self.lineage_id = kwargs.get('lineage_id')
        self.sample_quality = kwargs.get('sample_quality')

    @classmethod
    def gender_list(cls):
        _genders = set(genders)
        data = [(gender, gender) for gender in _genders]
        return data

    @classmethod
    def caste_list(cls):
        _castes = set(castes)
        data = [(caste, caste) for caste in _castes]
        return data

    @classmethod
    def stage_list(cls):
        _stages = set(stages)
        data = [(stage, stage) for stage in _stages]
        return data

class Genus(TaxonBase):

    __tablename__ = 'genus'

    genus_id            = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)
    name                = db.Column(db.String(128), nullable=False)

    def __init__(self, name, description):

        self.name = name
        self.description = description

    def specimens(self):
        return self._specimens

    @classmethod
    def select_list(cls):
        genera = cls.query.filter(cls.active == True)
        data = [(genus.id, genus.name) for genus in genera]
        data.insert(0,('',''))
        return data

    def __repr__(self):
        return '<Genus: ID={}, name={}>'.format(self.genus_id, self.name)

class Species(TaxonBase):

    __tablename__ = 'species'

    species_id          = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)

    def __init__(self, name, description):

        self.name = name
        self.description = description

    def specimens(self):
        return self._specimens

    @classmethod
    def select_list(cls):
        species = cls.query.filter(cls.active == True)
        data = [(specie.id, specie.name) for specie in species]
        data.insert(0,('',''))
        return data

    def __repr__(self):
        return '<Species: ID={}, name={}>'.format(self.species_id, self.name)

class Subspecies(TaxonBase):

    __tablename__ = 'subspecies'

    name                = db.Column(db.String(128), nullable=False)
    subspecies_id       = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)

    def __init__(self, name, description):

        self.name = name
        self.description = description

    def specimens(self):
        return self._specimens

    @classmethod
    def select_list(cls):
        subspecies = cls.query.filter(cls.active == True)
        data = [(subspecie.id, subspecie.name) for subspecie in subspecies]
        data.insert(0,('',''))
        return data

    def __repr__(self):
        return '<Subspecies: ID={}, name={}>'.format(self.subspecies_id, self.name)

class Lineage(TaxonBase):

    __tablename__ = 'lineage'

    name                = db.Column(db.String(128), nullable=False)
    lineage_id          = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)

    def __init__(self, name, description):

        self.name = name
        self.description = description

    def specimens(self):
        return self._specimens

    @classmethod
    def select_list(cls):
        lineages = cls.query.filter(cls.active == True)
        data = [(lineage.id, lineage.name) for lineage in lineages]
        data.insert(0,('',''))
        return data

    def __repr__(self):
        return '<Subspecies: ID={}, name={}>'.format(self.lineage_id, self.name)
