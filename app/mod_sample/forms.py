from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, RadioField, StringField, TextAreaField
from wtforms.validators import InputRequired, Optional
from app.mod_package.models import Location, Person
from app.mod_util.models import Country

from app.mod_sample.models import Sample, Genus, Species, Subspecies, Lineage

class SampleForm(FlaskForm):

    # sample data
    sender_source_id        = StringField('Sender\'s Source ID', validators=[InputRequired()])
    country_id              = SelectField('Country of origin', validators=[InputRequired()])
    locality                = StringField('Locality', validators=[Optional()])
    hive                    = StringField('Hive', validators=[Optional()])
    latitude                = StringField('Latitude', validators=[Optional()])
    longitude               = StringField('Longitude', validators=[Optional()])
    additional_gps_info     = StringField('Additional GPS info', validators=[Optional()])
    additional_info         = StringField('Additional info', validators=[Optional()])
    collector               = SelectField('Collected by', validators=[InputRequired()])
    processor               = SelectField('Processed by', validators=[InputRequired()])
    process_location        = SelectField('Processed at', validators=[InputRequired()])
    sample_date_sampled     = DateField('Date sampled', format='%d-%m-%Y', validators=[InputRequired()])
    sample_date_received    = DateField('Date received', format='%d-%m-%Y', validators=[InputRequired()])

    freezer                 = StringField('Freezer', validators=[Optional()])
    shelf                   = StringField('Shelf', validators=[Optional()])
    box                     = StringField('Box', validators=[Optional()])

    genus_id                = SelectField('Genus', validators=[InputRequired()])
    species_id              = SelectField('Species', validators=[InputRequired()])
    subspecies_id           = SelectField('Subspecies', validators=[InputRequired()])
    lineage_id              = SelectField('Lineage', validators=[InputRequired()])
    sample_quality          = RadioField('95% Ethanol', choices=[(1, 'Yes'),(0, 'No')], validators=[InputRequired()])
    gender                  = RadioField('Gender', validators=[InputRequired()])
    caste                   = RadioField('Caste', validators=[InputRequired()])
    stage                   = RadioField('Development stage', validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super(SampleForm, self).__init__(*args, **kwargs)
        self.country_id.choices         = Country.select_list()
        self.collector.choices          = Person.select_list(['C'])
        self.processor.choices          = Person.select_list(['P'])
        self.process_location.choices   = Location.select_list()
        self.genus_id.choices           = Genus.select_list()
        self.species_id.choices         = Species.select_list()
        self.subspecies_id.choices      = Subspecies.select_list()
        self.lineage_id.choices         = Lineage.select_list()
        self.gender.choices             = Sample.gender_list()
        self.caste.choices              = Sample.caste_list()
        self.stage.choices              = Sample.stage_list()
