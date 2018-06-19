from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, RadioField
from wtforms.validators import DataRequired, InputRequired, Optional
from app.mod_package.models import Courier, Partner, Location, Person
from app.mod_util.models import Country


class PackageForm(FlaskForm):
    # data to populate select fields
    couriers        = Courier.select_list()
    partners        = Partner.select_list()
    locations       = Location.select_list()
    persons         = Person.select_list()
    # countries       = Country.select_list()

    # package metadata definition
    package_id      = StringField('Package ID', validators=[InputRequired()])
    date_sent       = DateField('Date sent', format='%d-%m-%Y', validators=[InputRequired()])
    date_received   = DateField('Date received', format='%d-%m-%Y', validators=[InputRequired()])
    courier_id      = SelectField('Courier', choices=couriers, validators=[InputRequired()])
    partner_id      = SelectField('Partner', choices=partners, validators=[InputRequired()])
    location_id     = SelectField('Stored at', choices=locations, validators=[InputRequired()])
    sender_id       = SelectField('Sender', choices=persons, validators=[InputRequired()])
    receiver_id     = SelectField('Receiver', choices=persons, validators=[InputRequired()])
    tracking_number = StringField('Tracking number', validators=[InputRequired()])
    comments        = TextAreaField('Comments', validators=[Optional()])

    # utiliy
    # pack_country         = SelectField('Country', choices=countries, validators=[Optional()])
    # pack_state           = SelectField('State', choices=[], validators=[Optional()])
