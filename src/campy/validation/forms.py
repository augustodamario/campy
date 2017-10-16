# coding: utf-8
from campy.models import Advisor
from campy.models import Child
from campy.models import NATIONALITIES
from campy.models import Patient
from campy.models import PROVINCES
from campy.validation.validators import Coadvisors
from campy.validation.validators import DataAuto
from campy.validation.validators import DataOptional
from campy.validation.validators import DateRange
from campy.validation.validators import Entity
from campy.validation.validators import Telephone
from datetime import date
from datetime import datetime
from wtforms.fields import DateField
from wtforms.fields import DateTimeField
from wtforms.fields import Field
from wtforms.fields import FieldList
from wtforms.fields import IntegerField
from wtforms.fields import StringField
from wtforms.form import Form
from wtforms.validators import AnyOf
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Length
from wtforms.validators import NumberRange


# Hack WTForms: parse datetime given as dict value
def _datetimefield_process_data(self, value):
    self.data = None
    if value and not isinstance(value, datetime):
        try:
            self.data = datetime.strptime(value, self.format)
        except ValueError:
            raise ValueError(self.gettext("Not a valid datetime value"))
DateTimeField.process_data = _datetimefield_process_data


# Hack WTForms: parse date given as dict value
def _datefield_process_data(self, value):
    self.data = None
    if value and not isinstance(value, date):
        try:
            self.data = datetime.strptime(value, self.format).date()
        except ValueError:
            raise ValueError(self.gettext("Not a valid date value"))
DateField.process_data = _datefield_process_data


# Hack WTForms: parse integer given as dict value
def _integerfield_process_data(self, value):
    self.data = None
    if value:
        try:
            self.data = int(value)
        except ValueError:
            raise ValueError(self.gettext("Not a valid integer value"))
IntegerField.process_data = _integerfield_process_data


class BaseForm(Form):
    class Meta:
        locales = ["es_AR", "es"]


class AdvisorForm(BaseForm):
    id = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])


class ChildForm(BaseForm):
    modifiedon = DateTimeField(validators=[
                                   DataOptional(default=datetime.now),
                                   DateRange(min=datetime(1900, 1, 1), max=datetime.now)
                               ],
                               format="%Y-%m-%dT%H:%M:%SZ")
    name = StringField(validators=[DataRequired()])
    known_age = IntegerField(validators=[DataOptional(), NumberRange(min=0, max=99)])
    birthdate = DateField(validators=[DataOptional(), DateRange(min=date(1900, 1, 1), max=date.today)],
                          format="%Y-%m-%d")


class PatientForm(BaseForm):
    record = IntegerField(validators=[DataAuto(Patient), NumberRange(min=1)])
    firstname = StringField(validators=[DataRequired(), Length(min=2)])
    middlename = StringField(validators=[DataOptional()])
    surname = StringField(validators=[DataOptional(), Length(min=2)])
    birthdate = DateField(validators=[DataRequired(), DateRange(min=date(1900, 1, 1), max=date.today)],
                          format="%Y-%m-%d")
    nationality = StringField(validators=[DataRequired(), AnyOf(values=NATIONALITIES)])
    occupation = StringField(validators=[DataRequired(), Length(min=3)])
    children = FieldList(Field(validators=[DataOptional(), Entity(ChildForm, Child)]))
    cellphone = StringField(validators=[DataOptional(), Telephone()])
    cellphone2 = StringField(validators=[DataOptional(), Telephone()])
    telephone = StringField(validators=[DataOptional(), Telephone()])
    email = StringField(validators=[DataOptional(), Email()])
    province = StringField(validators=[DataOptional(), AnyOf(values=PROVINCES)])
    city = StringField(validators=[DataOptional(), Length(min=2)])
    district = StringField(validators=[DataOptional()])
    advisor = Field(validators=[DataOptional(), Entity(AdvisorForm, Advisor)])
    coadvisors = FieldList(Field(validators=[DataOptional(), Entity(AdvisorForm, Advisor)]), validators=[Coadvisors()])
    notes = StringField(validators=[DataOptional()])


# TODO remove
# relative_firstname = StringField(validators=[DataOptional(), Length(min=2)])
# relative_middlename = StringField(validators=[DataOptional()])
# relative_surname = StringField(validators=[DataOptional(), Length(min=2)])
# relative_relationship = StringField(validators=[DataOptional(), Length(min=2)])
# relative_cellphone = StringField(validators=[DataOptional(), Length(min=10)])
# relative_province = StringField(validators=[DataOptional(), AnyOf(values=PROVINCES)], filters=[lambda s: s or None])
# relative_city = StringField(validators=[DataOptional(), Length(min=2)])
# relative_district = StringField(validators=[DataOptional()])
