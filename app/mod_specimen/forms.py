from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, StringField, TextAreaField
from wtforms.validators import InputRequired, Optional
from app.mod_specimen.models import Specimen

class SpecimenForm(FlaskForm):

    measurements            = Specimen.measurement_list()
    # specimen data

    collection_sample_id    = StringField('WorldBEE Specimen ID', validators=[InputRequired()])
    dna                     = StringField('DNA ng/µl', validators=[Optional()])
    date_collected          = DateField('Date measured', format='%d-%m-%Y', validators=[Optional()])
    measurement             = RadioField('Measurement', choices=measurements, validators=[Optional()])
    body_part               = StringField('Body part used in DNA extraction', validators=[Optional()])
    specimen_freezer        = StringField('Specimen Freezer', validators=[InputRequired()])
    specimen_box            = StringField('Specimen Box', validators=[InputRequired()])
    dna_freezer             = StringField('DNA Freezer', validators=[Optional()])
    dna_box                 = StringField('DNA Box', validators=[Optional()])
    comments                = TextAreaField('Comments', validators=[Optional()])
