# coding: utf-8
from datetime import datetime
from wtforms.fields import DateField


# Hack WTForms: parse date given as dict value
def _datefield_process_data(self, value):
    self.data = None
    if value is not None:
        try:
            self.data = datetime.strptime(value, self.format).date()
        except ValueError:
            raise ValueError(self.gettext("Not a valid date value"))
DateField.process_data = _datefield_process_data
