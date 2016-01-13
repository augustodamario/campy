# coding: utf-8
from campy.security import get_current_branch
import re
from wtforms.validators import Optional
from wtforms.validators import StopValidation
from wtforms.validators import ValidationError


class DataOptional(Optional):
    def __call__(self, form, field):
        if not field.data or isinstance(field.data, basestring) and not self.string_check(field.data):
            field.errors[:] = []
            field.data = None
            raise StopValidation()


class DataAuto(object):
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, form, field):
        if field.data is None:
            cls = self.cls
            prop = field.name
            ancestor = get_current_branch().key
            results = cls.query(ancestor=ancestor).order(-getattr(cls, prop)).fetch(1, projection=[prop])
            field.data = (getattr(results[0], prop) + 1) if results else 1


class DateRange(object):
    __DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, min=None, max=None):
        if min is None and max is None:
            raise ValueError()
        self.min = min
        self.max = max

    def __call__(self, form, field):
        data = field.data
        if data is not None and\
                ((self.min is not None and data < self.min) or (self.max is not None and data > self.max)):
            if self.min is None:
                message = u"La fecha debe ser igual o anterior al %s." % self.max.strftime(self.__DATE_FORMAT)
            elif self.max is None:
                message = u"La fecha debe ser igual o posterior al %s." % self.min.strftime(self.__DATE_FORMAT)
            else:
                message = u"La fecha debe estar entre el %s y el %s." %\
                          (self.min.strftime(self.__DATE_FORMAT), self.max.strftime(self.__DATE_FORMAT))
            raise ValidationError(message)


class Telephone(object):
    __PATTERN = re.compile("^[0-9]{10,}$", 0)
    __MESSAGE = u"El campo debe tener al menos 10 números (acepta espacios)"

    def __init__(self, message=None):
        self.__message = message or self.__MESSAGE

    def __call__(self, form, field, message=None):
        text = field.data or ""
        match = self.__PATTERN.match(text.replace(" ", ""))
        if not match:
            if message is None:
                if self.__message is None:
                    message = field.gettext("Invalid input.")
                else:
                    message = self.__message
            raise ValidationError(message)
        return match


class Entity(object):
    __MESSAGE = u"El campo no es válido"

    def __init__(self, form, cls, message=None):
        self.form = form
        self.cls = cls
        self.message = message or self.__MESSAGE

    def __call__(self, form, field):
        entity_form = self.form(data=field.data)
        if not entity_form.validate():
            raise ValidationError(self.message)
        entity = self.cls()
        entity_form.populate_obj(entity)
        field.data = entity
