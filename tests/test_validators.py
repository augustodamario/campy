# coding: utf-8
from campy.validation.validators import DateRange
from campy.validation.validators import ValidationError
from datetime import date
from unittest import TestCase


class FieldMock(object):
    def __init__(self, data):
        self.data = data


class DateRangeTest(TestCase):
    def setUp(self):
        self.form = {}
        self.field = FieldMock(date(2000, 1, 1))

    def test_new_instance_should_fail(self):
        with self.assertRaises(ValueError):
            DateRange()

    def test_validation_should_succeed_when_no_data(self):
        self.field.data = None
        validator = DateRange(min=date(1999, 12, 31), max=date(2000, 1, 2))
        validator(self.form, self.field)

    def test_min_should_fail(self):
        validator = DateRange(min=date(2000, 1, 2))
        with self.assertRaises(ValidationError):
            validator(self.form, self.field)

    def test_min_should_succeed(self):
        validator = DateRange(min=date(2000, 1, 1))
        validator(self.form, self.field)

        validator = DateRange(min=date(1999, 12, 31))
        validator(self.form, self.field)

    def test_max_should_fail(self):
        validator = DateRange(max=date(1999, 12, 31))
        with self.assertRaises(ValidationError):
            validator(self.form, self.field)

    def test_max_should_succeed(self):
        validator = DateRange(max=date(2000, 1, 1))
        validator(self.form, self.field)

        validator = DateRange(max=date(2000, 1, 2))
        validator(self.form, self.field)

    def test_min_and_max_should_succeed(self):
        validator = DateRange(min=date(1999, 12, 31), max=date(2000, 1, 2))
        validator(self.form, self.field)
