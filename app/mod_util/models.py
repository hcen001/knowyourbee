from app import db

class Country(db.Model):

    __tablename__       = 'country'

    id          = db.Column(db.Integer, primary_key=True)
    alpha_code  = db.Column(db.String(3), nullable=False)
    name        = db.Column(db.String(128), nullable=False)
    phone_code  = db.Column(db.String(16), nullable=False)

    def __init__(self, **kwargs):
        pass

    def __repr__(self):
        return '<Country: Alpha code={}, name={}, phone_code={}>'.format(self.alpha_code, self.name, self.phone_code)

class State(db.Model):

    __tablename__       = 'state'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(128), nullable=False)
    country_id  = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    country     = db.relationship('Country', backref='states', foreign_keys=[country_id], lazy=True)

    def __init__(self, **kwargs):

        pass

    def __repr__(self):
        return '<State: name={}, country={}>'.format(self.name, self.country.name)

class City(db.Model):

    __tablename__       = 'city'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(128), nullable=False)
    state_id    = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    city       = db.relationship('State', backref='cities', foreign_keys=[state_id], lazy=True)

    def __init__(self, **kwargs):

        pass

    def __repr__(self):
        return '<City: name={}, state={}>'.format(self.name, self.state.name)
