from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, RadioField, StringField
from wtforms.validators import InputRequired, Optional
from app.mod_specimen.models import Specimen, Genus, Species, Subspecies, Lineage

class SpecimenForm(FlaskForm):

    genera      = Genus.select_list()
    species     = Species.select_list()
    subspecies  = Subspecies.select_list()
    lineage     = Lineage.select_list()

    genders     = Specimen.gender_list()
    castes      = Specimen.caste_list()
    stages      = Specimen.stage_list()

    # specimen data

    genus_id        = SelectField('Genus', choices=genera, validators=[InputRequired()])
    species_id      = SelectField('Species', choices=species, validators=[InputRequired()])
    subspecies_id   = SelectField('Subspecies', choices=subspecies, validators=[InputRequired()])
    lineage_id      = SelectField('Lineage', choices=lineage, validators=[InputRequired()])
    sample_quality  = RadioField('95% Ethanol', choices=[(1, 'Yes'),(0, 'No')], validators=[InputRequired()])
    gender          = RadioField('Gender', choices=genders, validators=[InputRequired()])
    caste           = RadioField('Caste', choices=castes, validators=[InputRequired()])
    stage           = RadioField('Development stage', choices=stages, validators=[InputRequired()])