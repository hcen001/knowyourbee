from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id           = db.Column(db.Integer, primary_key=True)
    date_created = db.Column('date_created', db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column('date_updated', db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    active       = db.Column('active', db.Boolean, default=True, server_default='t')

    def add_or_update(self, deactivate=False):

        if deactivate:
            self.active = False

        db.session.add(self)
        db.session.commit()

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
