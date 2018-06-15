from app import db

class PackageIndex(db.Model):

    __tablename__       = 'package_index'

    id               = db.Column(db.Integer, primary_key=True)
    prefix           = db.Column(db.String(64), nullable=False)
    next_suffix      = db.Column(db.Integer, nullable=False)

    def __init__(self, prefix):

        self.prefix = prefix

    def add_or_increase(self):

        index = self.query.filter(PackageIndex.prefix == self.prefix).first()

        if index is None:
            self.next_suffix = 1
            db.session.add(self)
        else:
            index.next_suffix += 1
            db.session.add(index)

        db.session.commit()

        return index if index is not None else self


class Country(db.Model):

    __tablename__       = 'country'

    id          = db.Column(db.Integer, primary_key=True)
    alpha_code  = db.Column(db.String(3), nullable=False)
    name        = db.Column(db.String(128), nullable=False)
    phone_code  = db.Column(db.String(16), nullable=False)

    def __init__(self, **kwargs):
        pass

    @classmethod
    def select_list(cls):

        data = cls.query.all()
        countries = [(country.id, country.name) for country in data]
        countries.insert(0,('',''))

        return countries

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

    @classmethod
    def select_list(cls, country):

        data = cls.query.filter(State.country_id == country)
        states = [{"id": state.id, "text": state.name} for state in data]
        states.insert(0,{"id": "","text": ""})

        return states

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

    @classmethod
    def select_list(cls, state):

        data = cls.query.filter(City.state_id == state)
        cities = [{"id": city.id, "text": city.name} for city in data]
        cities.insert(0,{"id": "","text": ""})

        return cities

    def __repr__(self):
        return '<City: name={}, state={}>'.format(self.name, self.state.name)
