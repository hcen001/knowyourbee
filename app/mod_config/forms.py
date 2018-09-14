from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms import widgets
from wtforms.validators import DataRequired, InputRequired, Optional, Email

class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CollaboratorForm(FlaskForm):

    first_name          = StringField('First name', validators=[InputRequired()])
    last_name           = StringField('Last name', validators=[InputRequired()])
    email               = EmailField('Email', validators=[InputRequired(), Email()])
    phone               = StringField('Phone', validators=[Optional()])
    roles               = Select2MultipleField('Roles', validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super(CollaboratorForm, self).__init__(*args, **kwargs)
        self.roles.choices  = [('S','Sender'),('C','Collector'),('R','Receiver'),('P','Processor')]

class PartnerForm(FlaskForm):

    first_name          = StringField('First name', validators=[InputRequired()])
    last_name           = StringField('Last name', validators=[InputRequired()])
    email               = EmailField('Email', validators=[InputRequired(), Email()])
    institution         = StringField('Institution', validators=[InputRequired()])
    phone               = StringField('Phone', validators=[InputRequired()])

class LocationForm(FlaskForm):

    name                = StringField('Name', validators=[InputRequired()])
    description         = TextAreaField('Description', validators=[InputRequired()])

class CourierForm(FlaskForm):

    name                = StringField('Name', validators=[InputRequired()])
    description         = TextAreaField('Description', validators=[InputRequired()])
