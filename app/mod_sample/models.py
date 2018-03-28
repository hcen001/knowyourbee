from app.models import Base
from app.mod_package.models import Package, Person, Location
from app.mod_specimen.models import Specimen
from app import db

class Sample(Base):

    __tablename__       = 'sample'


    # Sample & Package inspection data
    package_id          = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    collector_id        = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    processor_id        = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    process_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    date_sampled        = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    date_received       = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    sample_quality      = db.Column(db.Boolean, default=True, server_default='t', nullable=False)

    #Sample data and location
    origin_country      = db.Column(db.String(128), nullable=False)
    origin_state        = db.Column(db.String(128), nullable=False)
    origin_city         = db.Column(db.String(128), nullable=False)
    origin_locality     = db.Column(db.String(128), nullable=True)
    hive                = db.Column(db.String(64), nullable=True)
    latitude            = db.Column()
    longitude           = db.Column()
    additional_gps_info = db.Column()
    additional_info     = db.Column()

    #Preliminary identification sent by collaborator


    #Sample storage location
    freezer             = db.Column(db.String(32), nullable=False)
    shelf               = db.Column(db.String(32), nullable=False)
    box                 = db.Column(db.String(32), nullable=False)

    #Relationships
    package             = db.relationship('Package', back_populates='samples', foreign_keys=[package_id], lazy=True)
    collector           = db.relationship('Person', backref='samples', foreign_keys=[collector_id], lazy=True)
    processor           = db.relationship('Person', backref='processed_samples', foreign_keys=[processor_id], lazy=True)
    process_location    = db.relationship('Location', backref='samples', foreign_keys=[process_location_id], lazy=True)

    specimens           = db.relationship('Specimen', back_populates='sample')

    def __init__(self):

        pass

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
