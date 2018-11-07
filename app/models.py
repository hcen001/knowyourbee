from app import db
from sqlalchemy.exc import IntegrityError

import json
import datetime

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id           = db.Column(db.Integer, primary_key=True)
    date_created = db.Column('date_created', db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column('date_updated', db.DateTime, default=db.func.current_timestamp(), onupdate=datetime.datetime.now)
    active       = db.Column('active', db.Boolean, default=True, server_default='t')

    def add_or_update(self, deactivate=None):

        if deactivate is not None and deactivate == True:
            self.active = True

        if deactivate is not None and deactivate == False:
            self.active = False

        try:
            # print('DIR', dir(self))
            db.session.add(self)
            # print(self.__dict__)
            # print(self.__dict__)
            # db.session.execute(self.__table__.insert(values=self.__dict__, prefixes=['OR IGNORE']))
            db.session.flush()
        except IntegrityError as e:
            raise

    def update(self, data):
        self.query.update(data)

    def save(self):
        db.session.commit()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class PersonBase(Base):

    __abstract__ = True

    fname = db.Column('fname', db.String(128), nullable=False, default='First name', server_default='First name')
    lname = db.Column('lname', db.String(128), nullable=False, default='Last name', server_default='Last name')
    email = db.Column('email', db.String(128), nullable=False, default='someone@xample.org', server_default='someone@xample.org', unique=True)
    phone = db.Column('phone', db.String(128), nullable=False, default='N/A', server_default='N/A')

    @property
    def full_name(self):
        return self.fname+' '+self.lname

class TaxonBase(Base):

    __abstract__ = True

    name                = db.Column(db.String(128), nullable=False)
    description         = db.Column(db.String(512), nullable=True)
