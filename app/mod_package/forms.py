from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, RadioField
from wtforms.validators import DataRequired, InputRequired, Optional
from app.mod_package.models import Courier, Partner, Location, Person
from app.mod_util.models import Country

# data to populate select fields
# couriers        = Courier.select_list()
# partners        = Partner.select_list()
# locations       = Location.select_list()
# senders         = Person.select_list(['S'])
# receivers       = Person.select_list(['R'])

class PackageForm(FlaskForm):

    # package metadata definition
    package_id      = StringField('Package ID', validators=[InputRequired()])
    date_sent       = DateField('Date sent', format='%d-%m-%Y', validators=[InputRequired()])
    date_received   = DateField('Date received', format='%d-%m-%Y', validators=[InputRequired()])
    courier_id      = SelectField('Courier', validators=[InputRequired()])
    partner_id      = SelectField('Partner', validators=[InputRequired()])
    location_id     = SelectField('Stored at', validators=[InputRequired()])
    sender_id       = SelectField('Sender', validators=[InputRequired()])
    receiver_id     = SelectField('Receiver', validators=[InputRequired()])
    tracking_number = StringField('Tracking number', validators=[Optional()])
    comments        = TextAreaField('Comments', validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        self.courier_id.choices     = Courier.select_list()
        self.partner_id.choices     = Partner.select_list()
        self.location_id.choices    = Location.select_list()
        self.sender_id.choices      = Person.select_list(['S'])
        self.receiver_id.choices    = Person.select_list(['R'])
