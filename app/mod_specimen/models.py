from app.models import Base
from app.mod_sample.models import Sample
from app import db

from sqlalchemy.dialects.postgresql import ENUM

measurements = ('qubit', 'nanodrop')

class Specimen(Base):

    __tablename__ = 'specimen'

    collection_sample_id    = db.Column(db.String(32), nullable=False, default='122', server_default='122')
    dna                     = db.Column(db.Float, nullable=True)
    date_collected          = db.Column(db.DateTime, nullable=True)
    measurement             = db.Column(ENUM(*measurements, name='measurement_enum'), nullable=True)
    body_part               = db.Column(db.String(128), nullable=True)
    freezer                 = db.Column(db.String(32), nullable=True)
    box                     = db.Column(db.String(32), nullable=True)
    comments                = db.Column(db.String(1024), nullable=True)

    sample_id               = db.Column(db.Integer, db.ForeignKey('sample.id'), nullable=False)

    # Relationships
    sample                  = db.relationship('Sample', back_populates='specimens', foreign_keys=[sample_id])

    def __init__(self, **kwargs):

        self.sample_id              = kwargs.get('sample_id')
        self.collection_sample_id   = kwargs.get('collection_sample_id') or None
        self.dna                    = kwargs.get('dna') or None
        self.date_collected         = kwargs.get('date_collected') or None
        self.measurement            = kwargs.get('measurement') or None
        self.body_part              = kwargs.get('body_part') or None
        self.freezer                = kwargs.get('freezer') or None
        self.box                    = kwargs.get('box') or None
        self.comments               = kwargs.get('comments') or None

    @classmethod
    def measurement_list(cls):
        _measurements = set(measurements)
        data = [(measurement, measurement) for measurement in _measurements]
        return data

    def __repr__(self):
        return '<Specimen: Collection ID={}, Date collected={}, Freezer={}, Box={}>'.format(self.collection_sample_id, self.date_collected, self.freezer, self.box)
