# coding: utf-8
from datetime import datetime
from wtforms.fields import DateField
from wtforms.fields import IntegerField


# Hack WTForms: parse date given as dict value
def _datefield_process_data(self, value):
    self.data = None
    if value:
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
