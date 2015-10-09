# coding: utf-8
from campy.models import NATIONALITIES
from campy.models import PROVINCES
from campy.validation.validators import DataOptional
from campy.validation.validators import DateRange
from datetime import date
from wtforms.fields import DateField
from wtforms.fields import StringField
from wtforms.form import Form
from wtforms.validators import AnyOf
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Length


class BaseForm(Form):
    class Meta:
        locales = ["es_AR", "es"]


class PatientForm(BaseForm):
    firstname = StringField(validators=[DataRequired(), Length(min=2)])
    middlename = StringField(validators=[DataOptional()])
    surname = StringField(validators=[DataRequired(), Length(min=2)])
    birthdate = DateField(validators=[DataRequired(), DateRange(min=date(1900, 1, 1), max=date.today())],
                          format="%Y-%m-%d")
    nationality = StringField(validators=[DataRequired(), AnyOf(values=NATIONALITIES)])
    cellphone = StringField(validators=[DataOptional(), Length(min=10)])
    email = StringField(validators=[DataOptional(), Email()])
    province = StringField(validators=[DataRequired(), AnyOf(values=PROVINCES)])
    city = StringField(validators=[DataRequired(), Length(min=2)])
    district = StringField(validators=[DataOptional()])
    relative_firstname = StringField(validators=[DataOptional(), Length(min=2)])
    relative_middlename = StringField(validators=[DataOptional()])
    relative_surname = StringField(validators=[DataOptional(), Length(min=2)])
    relative_relationship = StringField(validators=[DataOptional(), Length(min=2)])
    relative_cellphone = StringField(validators=[DataOptional(), Length(min=10)])
    relative_province = StringField(validators=[DataOptional(), AnyOf(values=PROVINCES)], filters=[lambda s: s or None])
    relative_city = StringField(validators=[DataOptional(), Length(min=2)])
    relative_district = StringField(validators=[DataOptional()])
    notes = StringField(validators=[DataOptional()])
