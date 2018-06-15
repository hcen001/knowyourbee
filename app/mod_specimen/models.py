from app.models import Base
from app.mod_sample.models import Sample
from app import db

measurements = ('qubit', 'nanodrop')

class Specimen(Base):

    __tablename__ = 'specimen'

    collection_sample_id    = db.Column(db.String(32), nullable=False, default='122', server_default='122')
    sample_id               = db.Column(db.Integer, db.ForeignKey('sample.id'), nullable=False)

    def __init__(self, **kwargs):
        pass

    @classmethod
    def measurement_list(cls):
        _measurements = set(measurements)
        data = [(measurement, measurement) for measurement in _measurements]
        return data
