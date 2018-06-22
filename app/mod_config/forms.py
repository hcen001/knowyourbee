from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms import widgets
from wtforms.validators import DataRequired, InputRequired, Optional, Email

collab_roles = [('S','Sender'),('C','Collector'),('R','Receiver'),('P','Processor')]

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
    phone               = StringField('Phone', validators=[InputRequired()])
    roles               = Select2MultipleField('Roles', choices=collab_roles, validators=[InputRequired()])
