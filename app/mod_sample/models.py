from app.models import Base
from app.mod_package.models import Package, Person, Location
from app import db

from geoalchemy2.types import Geometry

from app.mod_util.utils import GUID
import uuid

db.GUID = GUID

class Sample(Base):

    __tablename__       = 'sample'

    sample_id           = db.Column(db.GUID(), default=uuid.uuid1(), nullable=False)

    # Sample & Package inspection data
    package_id          = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    collector_id        = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    processor_id        = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    process_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    date_sampled        = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    date_received       = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    #Sample data and location
    sender_source_id        = db.Column(db.String(32), nullable=False)
    origin_country          = db.Column(db.String(128), nullable=True)
    origin_state            = db.Column(db.String(128), nullable=True)
    origin_city             = db.Column(db.String(128), nullable=True)
    origin_locality         = db.Column(db.String(128), nullable=True)
    hive                    = db.Column(db.String(64), nullable=True)
    coordinates             = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    additional_gps_info     = db.Column(db.String(1024), nullable=True)
    additional_info         = db.Column(db.String(1024), nullable=True)
    comments                = db.Column(db.String(1024), nullable=True)

    #Preliminary identification sent by collaborator

    #Sample storage location
    freezer             = db.Column(db.String(32), nullable=True)
    shelf               = db.Column(db.String(32), nullable=True)
    box                 = db.Column(db.String(32), nullable=True)

    #Relationships
    package             = db.relationship('Package', backref='_samples', foreign_keys=[package_id], lazy=True)
    collector           = db.relationship('Person', backref='_collected_samples', foreign_keys=[collector_id], lazy=True)
    processor           = db.relationship('Person', backref='_processed_samples', foreign_keys=[processor_id], lazy=True)
    process_location    = db.relationship('Location', backref='_samples', foreign_keys=[process_location_id], lazy=True)

    def __init__(self, **kwargs):

        self.package_id = kwargs.get('package_id')
        self.collector_id = kwargs.get('collector')
        self.processor_id = kwargs.get('processor')
        self.process_location_id = kwargs.get('process_location')
        self.date_sampled = kwargs.get('sample_date_sampled')
        self.date_received = kwargs.get('sample_date_received')
        self.sender_source_id = kwargs.get('sender_source_id')
        self.origin_country = kwargs.get('origin_country')
        self.origin_state = kwargs.get('origin_state')
        self.origin_locality = kwargs.get('origin_locality')
        self.hive = kwargs.get('hive')
        self.coordinates = kwargs.get('coordinates')
        self.additional_gps_info = kwargs.get('additional_gps_info')
        self.additional_info = kwargs.get('additional_info')
        self.comments = kwargs.get('comments')
        self.freezer = kwargs.get('freezer')
        self.shelf = kwargs.get('shelf')
        self.box = kwargs.get('box')

    def collected_by(self):
        return self.collector

    def project_partner(self):
        return self.package.partner

    def processed_by(self):
        return self.processor

    def processed_at(self):
        return self.process_location

    def specimens_in_vial(self):
        return self._specimens

    def number_of_specimens_in_vial(self):
        return len(self.specimens_in_vial())

    def sample_quality(self):
        return self.sample_quality

    def __repr__(self):
        return '<Sample: ID={}>'.format(self.sample_id)

# from app.mod_specimen.models import Specimen
