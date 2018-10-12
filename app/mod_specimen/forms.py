from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, StringField, TextAreaField, DecimalField, SelectField
# from wtforms.widgets.html5 import NumberInput
from wtforms.validators import InputRequired, Optional
from app.mod_specimen.models import Specimen, DNAMeasurement


class SpecimenForm(FlaskForm):

    # specimen data

    collection_sample_id    = StringField('WorldBEE Specimen ID', validators=[InputRequired()])
    dna                     = DecimalField('DNA ng/µl', validators=[Optional()])
    date_collected          = DateField('Date measured', format='%d-%m-%Y', validators=[Optional()])
    measurement_id          = SelectField('Measurement', validators=[Optional()])
    body_part               = StringField('Body part used in DNA extraction', validators=[Optional()])
    specimen_freezer        = StringField('Specimen Freezer', validators=[InputRequired()])
    specimen_box            = StringField('Specimen Box', validators=[InputRequired()])
    dna_freezer             = StringField('DNA Freezer', validators=[Optional()])
    dna_box                 = StringField('DNA Box', validators=[Optional()])
    comments                = TextAreaField('Comments', validators=[Optional()])

    def __init__(self, *args, **kwargs):

        super(SpecimenForm, self).__init__(*args, **kwargs)
        self.measurement_id.choices = DNAMeasurement.select_list()
