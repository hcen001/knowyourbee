from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, RadioField, StringField, TextAreaField
from wtforms.validators import InputRequired, Optional
from app.mod_package.models import Location, Person
from app.mod_util.models import Country

from app.mod_sample.models import Sample, Genus, Species, Subspecies, Lineage

class SampleForm(FlaskForm):

    locations       = Location.select_list()
    collectors      = Person.select_list(['C'])
    processors      = Person.select_list(['P'])
    countries       = Country.select_list()

    genera          = Genus.select_list()
    species         = Species.select_list()
    subspecies      = Subspecies.select_list()
    lineage         = Lineage.select_list()

    genders         = Sample.gender_list()
    castes          = Sample.caste_list()
    stages          = Sample.stage_list()

    # sample data
    sender_source_id        = StringField('Sender\'s Source ID', validators=[InputRequired()])
    country                 = SelectField('Country of origin', choices=countries, validators=[InputRequired()])
    # state                   = SelectField('State or Province', choices=[], validators=[InputRequired()])
    # city                    = SelectField('City', choices=[], validators=[InputRequired()])
    locality                = StringField('Locality', validators=[Optional()])
    hive                    = StringField('Hive', validators=[Optional()])
    latitude                = StringField('Latitude', validators=[Optional()])
    longitude               = StringField('Longitude', validators=[Optional()])
    additional_gps_info     = StringField('Additional GPS info', validators=[Optional()])
    additional_info         = StringField('Additional info', validators=[Optional()])
    # comments                = TextAreaField('Comments', validators=[Optional()])
    collector               = SelectField('Collected by', choices=collectors, validators=[InputRequired()])
    processor               = SelectField('Processed by', choices=processors, validators=[InputRequired()])
    process_location        = SelectField('Processed at', choices=locations, validators=[InputRequired()])
    sample_date_sampled     = DateField('Date sampled', format='%d-%m-%Y', validators=[InputRequired()])
    sample_date_received    = DateField('Date received', format='%d-%m-%Y', validators=[InputRequired()])

    freezer                 = StringField('Freezer', validators=[Optional()])
    shelf                   = StringField('Shelf', validators=[Optional()])
    box                     = StringField('Box', validators=[Optional()])

    country_id              = SelectField('Country of origin', choices=countries, validators=[InputRequired()])
    # state_id                = SelectField('State/Province', choices=[], validators=[Optional()])
    # city_id                 = SelectField('City', choices=[], validators=[Optional()])
    # state                   = StringField('State/Province', validators=[Optional()])
    genus_id                = SelectField('Genus', choices=genera, validators=[InputRequired()])
    species_id              = SelectField('Species', choices=species, validators=[InputRequired()])
    subspecies_id           = SelectField('Subspecies', choices=subspecies, validators=[InputRequired()])
    lineage_id              = SelectField('Lineage', choices=lineage, validators=[InputRequired()])
    sample_quality          = RadioField('95% Ethanol', choices=[(1, 'Yes'),(0, 'No')], validators=[InputRequired()])
    gender                  = RadioField('Gender', choices=genders, validators=[InputRequired()])
    caste                   = RadioField('Caste', choices=castes, validators=[InputRequired()])
    stage                   = RadioField('Development stage', choices=stages, validators=[InputRequired()])
