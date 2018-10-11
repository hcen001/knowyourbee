from app.models import Base, TaxonBase
from app.mod_package.models import Package, Person, Location
from app import db

# from geoalchemy2.types import Geometry
from sqlalchemy.dialects.postgresql import ENUM

# from app.mod_util.utils import GUID
# import uuid

# db.GUID = GUID

genders = ('male', 'female')
castes = ('drone', 'worker', 'queen')
stages = ('egg', 'pupae', 'larvae', 'nymph', 'adult')

class Sample(Base):

    __tablename__       = 'sample'

    # sample_id           = db.Column(db.String(64), nullable=False)

    # Sample & Package inspection data
    package_id          = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    collector_id        = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    processor_id        = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    process_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    date_sampled        = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    date_received       = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    sample_quality      = db.Column(db.Boolean, default=True, server_default='t', nullable=False)
    gender              = db.Column(ENUM(*genders, name='gender_enum'), nullable=False)
    caste               = db.Column(ENUM(*castes, name='caste_enum'), nullable=False)
    development_stage   = db.Column(ENUM(*stages, name='dev_stage_enum'), nullable=False)
    genus_id            = db.Column(db.Integer, db.ForeignKey('genus.id'), nullable=False)
    species_id          = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)
    subspecies_id       = db.Column(db.Integer, db.ForeignKey('subspecies.id'), nullable=False)
    lineage_id          = db.Column(db.Integer, db.ForeignKey('lineage.id'), nullable=False)
    origin_country      = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=True)

    #Sample data and location
    sender_source_id        = db.Column(db.String(32), nullable=False)
    origin_locality         = db.Column(db.String(128), nullable=True)
    hive                    = db.Column(db.String(64), nullable=True)
    latitude                = db.Column(db.Float, nullable=True)
    longitude               = db.Column(db.Float, nullable=True)
    additional_gps_info     = db.Column(db.String(1024), nullable=True)
    additional_info         = db.Column(db.String(1024), nullable=True)

    #Preliminary identification sent by collaborator

    #Relationships
    collector           = db.relationship('Person', backref='_collected_samples', foreign_keys=[collector_id], lazy=True)
    processor           = db.relationship('Person', backref='_processed_samples', foreign_keys=[processor_id], lazy=True)
    process_location    = db.relationship('Location', backref='_samples', foreign_keys=[process_location_id], lazy=True)
    country             = db.relationship('Country', backref='_samples', foreign_keys=[origin_country], lazy=True)
    genus               = db.relationship('Genus', backref='_samples', foreign_keys=[genus_id], lazy=True)
    species             = db.relationship('Species', backref='_samples', foreign_keys=[species_id], lazy=True)
    subspecies          = db.relationship('Subspecies', backref='_samples', foreign_keys=[subspecies_id], lazy=True)
    lineage             = db.relationship('Lineage', backref='_samples', foreign_keys=[lineage_id], lazy=True)

    package             = db.relationship('Package', back_populates='samples', foreign_keys=[package_id])
    specimens           = db.relationship('Specimen', back_populates='sample')

    def __init__(self, **kwargs):

        self.package_id = kwargs.get('package_id')
        self.collector_id = kwargs.get('collector')
        self.processor_id = kwargs.get('processor')
        self.process_location_id = kwargs.get('process_location')
        self.date_sampled = kwargs.get('sample_date_sampled')
        self.date_received = kwargs.get('sample_date_received')
        self.sample_quality = True if kwargs.get('sample_quality') == 1 else False
        self.gender = kwargs.get('gender')
        self.caste = kwargs.get('caste')
        self.development_stage = kwargs.get('stage')
        self.genus_id = kwargs.get('genus_id')
        self.species_id = kwargs.get('species_id')
        self.subspecies_id = kwargs.get('subspecies_id')
        self.lineage_id = kwargs.get('lineage_id')
        self.origin_country = kwargs.get('country_id') or None
        self.sender_source_id = kwargs.get('sender_source_id')
        self.origin_locality = kwargs.get('origin_locality') or None
        self.hive = kwargs.get('hive') or None
        self.latitude = kwargs.get('latitude') or None
        self.longitude = kwargs.get('longitude') or None
        self.additional_gps_info = kwargs.get('additional_gps_info') or None
        self.additional_info = kwargs.get('additional_info') or None

    def collected_by(self):
        return self.collector

    def project_partner(self):
        return self.package.partner

    def processed_by(self):
        return self.processor

    def processed_at(self):
        return self.process_location

    def specimens_in_vial(self):
        return len(self.specimens)

    def number_of_specimens_in_vial(self):
        return len(self.specimens_in_vial())

    def sample_quality(self):
        return self.sample_quality

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

    def __repr__(self):
        return '<Sample: ID={}>'.format(self.sender_source_id)

class Genus(TaxonBase):

    __tablename__ = 'genus'

    # genus_id            = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)
    # name                = db.Column(db.String(128), nullable=False)

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

    # species_id          = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)

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

    # name                = db.Column(db.String(128), nullable=False)
    # subspecies_id       = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)

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

    # name                = db.Column(db.String(128), nullable=False)
    # lineage_id          = db.Column(db.GUID(), default=uuid.uuid4(), nullable=False)

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

# from app.mod_specimen.models import Specimen
