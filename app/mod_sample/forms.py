from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, RadioField, StringField, TextAreaField
from wtforms.validators import InputRequired, Optional
from app.mod_package.models import Location, Person

class SampleForm(FlaskForm):

    locations       = Location.select_list()
    persons         = Person.select_list()

    # sample data
    sender_source_id        = StringField('Sender\'s Source ID', validators=[InputRequired()])
    country                 = SelectField('Country of origin', choices=[], validators=[InputRequired()])
    state                   = SelectField('State or Province', choices=[], validators=[InputRequired()])
    city                    = SelectField('City', choices=[], validators=[InputRequired()])
    locality                = StringField('Locality', validators=[Optional()])
    hive                    = StringField('Hive', validators=[Optional()])
    coordinates             = StringField('Coordinates', validators=[Optional()])
    additional_gps_info     = StringField('Additional GPS info', validators=[Optional()])
    additional_info         = StringField('Additional info', validators=[Optional()])
    comments                = TextAreaField('Comments', validators=[Optional()])
    collector               = SelectField('Collected by', choices=persons, validators=[InputRequired()])
    processor               = SelectField('Processed by', choices=persons, validators=[InputRequired()])
    process_location        = SelectField('Processed at', choices=locations, validators=[InputRequired()])
    sample_date_sampled     = DateField('Date sampled', format='%d-%m-%Y', validators=[InputRequired()])
    sample_date_received    = DateField('Date received', format='%d-%m-%Y', validators=[InputRequired()])

    freezer                 = StringField('Freezer', validators=[Optional()])
    shelf                   = StringField('Shelf', validators=[Optional()])
    box                     = StringField('Box', validators=[Optional()])