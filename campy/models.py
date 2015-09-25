# coding: utf-8
from datetime import datetime
from google.appengine.ext.ndb import DateProperty
from google.appengine.ext.ndb import Model
from google.appengine.ext.ndb import StringProperty
from google.appengine.ext.ndb import TextProperty


class BaseModel(Model):
    def __convert(self, key, value):
        prop = self._properties[key]
        if isinstance(prop, DateProperty) and isinstance(value, (str, unicode)):
            return datetime.strptime(value[:10], "%Y-%m-%d").date()
        return value

    def from_dict(self, dic):
        dic = {k: self.__convert(k, v) for (k, v) in dic.iteritems() if k in self._properties}
        self.populate(**dic)
        return self


class Patient(BaseModel):
    firstname = StringProperty(required=True)
    middlename = StringProperty()
    surname = StringProperty()
    birthdate = DateProperty(required=True, indexed=False)
    nationality = StringProperty(indexed=False)
    cellphone = StringProperty()
    email = StringProperty()
    notes = TextProperty()
