# coding: utf-8
from campy.models import NATIONALITIES
from campy.models import PROVINCES
from datetime import datetime
from wtforms.fields import DateField
from wtforms.fields import StringField
from wtforms.form import Form
from wtforms.validators import AnyOf
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Length
from wtforms.validators import Optional
from wtforms.validators import StopValidation


# Hack WTForms: parse date given as dict value
def _datefield_process_data(self, value):
    self.data = None
    if value is not None:
        try:
            self.data = datetime.strptime(value, self.format).date()
        except ValueError:
            raise ValueError(self.gettext("Not a valid date value"))
DateField.process_data = _datefield_process_data


class DataOptional(Optional):
    def __call__(self, form, field):
        if not field.data or isinstance(field.data[0], basestring) and not self.string_check(field.data[0]):
            field.errors[:] = []
            raise StopValidation()


class BaseForm(Form):
    class Meta:
        locales = ["es_AR", "es"]


class PatientForm(BaseForm):
    firstname = StringField(validators=[DataRequired(), Length(min=2)])
    middlename = StringField(validators=[DataOptional(), Length(min=2)])
    surname = StringField(validators=[DataRequired(), Length(min=2)])
    birthdate = DateField(validators=[DataRequired()], format="%Y-%m-%d")
    nationality = StringField(validators=[DataRequired(), AnyOf(values=NATIONALITIES)])
    cellphone = StringField(validators=[DataOptional(), Length(min=10)])
    email = StringField(validators=[DataOptional(), Email()])
    province = StringField(validators=[DataRequired(), AnyOf(values=PROVINCES)])
    city = StringField(validators=[DataRequired(), Length(min=2)])
    district = StringField(validators=[DataOptional()])
    notes = StringField(validators=[DataOptional()])
