from app.models import Base
# from app.mod_sample.models import Sample
from app import db

class Specimen(Base):

    __tablename__ = 'specimen'

    sample_id           = db.Column(db.Integer, db.ForeignKey('sample.id'), nullable=False)

    sample              = db.relationship('Sample', back_populates='specimens', foreign_keys=[sample_id], lazy=True)

    def __init__(self, arg):

        self.arg = arg
