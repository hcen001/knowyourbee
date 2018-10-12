from app.models import Base, TaxonBase
from app.mod_sample.models import Sample
from app import db

from sqlalchemy.dialects.postgresql import ENUM

measurements = ('qubit', 'nanodrop')

class Specimen(Base):

    __tablename__ = 'specimen'

    collection_sample_id    = db.Column(db.String(32), nullable=False, default='122', server_default='122')
    dna                     = db.Column(db.Float, nullable=True)
    date_collected          = db.Column(db.DateTime, nullable=True)
    measurement_id          = db.Column(db.Integer, db.ForeignKey('measurement.id'), nullable=True)
    body_part               = db.Column(db.String(128), nullable=True)
    specimen_freezer        = db.Column(db.String(32), nullable=False)
    specimen_box            = db.Column(db.String(32), nullable=False)
    dna_freezer             = db.Column(db.String(32), nullable=True)
    dna_box                 = db.Column(db.String(32), nullable=True)
    comments                = db.Column(db.String(1024), nullable=True)

    sample_id               = db.Column(db.Integer, db.ForeignKey('sample.id'), nullable=False)

    # Relationships
    sample                  = db.relationship('Sample', back_populates='specimens', foreign_keys=[sample_id])
    measurement             = db.relationship('DNAMeasurement', backref='_specimens', foreign_keys=[measurement_id], lazy=True)

    def __init__(self, **kwargs):

        self.sample_id              = kwargs.get('sample_id')
        self.collection_sample_id   = kwargs.get('collection_sample_id')
        self.dna                    = kwargs.get('dna') or None
        self.measurement_id         = kwargs.get('measurement_id') or None
        self.date_collected         = kwargs.get('date_collected') or None
        self.body_part              = kwargs.get('body_part') or None
        self.specimen_freezer       = kwargs.get('specimen_freezer')
        self.specimen_box           = kwargs.get('specimen_box')
        self.dna_freezer            = kwargs.get('dna_freezer') or None
        self.dna_box                = kwargs.get('dna_box') or None
        self.comments               = kwargs.get('comments') or None

    def __repr__(self):
        return '<Specimen: Collection ID={}, Date collected={}, Freezer={}, Box={}>'.format(
            self.collection_sample_id, self.date_collected, self.specimen_freezer, self.specimen_box)

class DNAMeasurement(TaxonBase):

    __tablename__ = 'measurement'

    def __init__(self, name, description):
        super(DNAMeasurement, self).__init__()
        self.name = name
        self.description = description

    @classmethod
    def select_list(cls):
        measurements = cls.query.filter(cls.active == True)
        data = [(measurement.id, measurement.name) for measurement in measurements]
        data.insert(0,('',''))
        return data

    def __repr__(self):
        return '<Measurement: ID={}, name={}>'.format(self.id, self.name)
