from app.models import Base, Person
from app import db

class Package(Base):

    __tablename__       = 'package'

    date_sent           = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    date_received       = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    process_location    = db.Column(db.String(128), nullable=False)
    comments            = db.Column(db.String(512))
    carrier             = db.Column(db.String(64))

    partner_id          = db.Column(db.Integer, db.ForeignKey('partner.id'), nullable=False)

    def __init__(self, arg):
        self.arg = arg

class Partner(Person):

    __tablename__    = 'partner'

    institution      = db.Column(db.String(256))

    packages         = db.relationship('Package', backref='packages', lazy=True)

    def __init__(self, fname, lname, email, institution, phone):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.institution = institution
        self.phone = phone

    def __repr__(self):
        return '<Partner: fname={}, lname={}, email={}, institution={}, phone={}>'.format(self.fname, self.lname, self.email, self.institution, self.phone)

