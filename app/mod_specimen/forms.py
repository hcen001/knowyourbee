from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, StringField
from wtforms.validators import InputRequired, Optional
from app.mod_specimen.models import Specimen

class SpecimenForm(FlaskForm):

    measurements            = Specimen.measurement_list()
    # specimen data

    collection_sample_id    = StringField('Sample ID', validators=[InputRequired()])
    dna                     = StringField('DNA ng/ml', validators=[InputRequired()])
    date_collected          = DateField('Date collected', format='%d-%m-%Y', validators=[InputRequired()])
    measurement             = RadioField('Measurement', choices=measurements, validators=[InputRequired()])
    body_part               = StringField('Body part used in DNA extraction', validators=[InputRequired()])
    freezer                 = StringField('Freezer', validators=[InputRequired()])
    box                     = StringField('Box', validators=[InputRequired()])
