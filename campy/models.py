# coding: utf-8
from datetime import date
from google.appengine.ext.ndb import DateProperty
from google.appengine.ext.ndb import Model
from google.appengine.ext.ndb import StringProperty
from google.appengine.ext.ndb import TextProperty


class BaseModel(Model):
    def to_dict(self):
        d = super(BaseModel, self).to_dict()
        d["id"] = self.key.id()
        return d


class Patient(BaseModel):
    firstname = StringProperty(required=True)
    middlename = StringProperty()
    surname = StringProperty(required=True)
    birthdate = DateProperty(required=True, indexed=False)
    nationality = StringProperty(indexed=False)
    cellphone = StringProperty()
    email = StringProperty()
    notes = TextProperty()

    def age(self):
        if self.birthdate:
            # TODO replace with precise algorithm
            return int((date.today() - self.birthdate).total_seconds() / (365.2425 * 24 * 60 * 60))
        return None

    def to_dict(self):
        d = super(Patient, self).to_dict()
        d["birthdate"] = None if not self.birthdate else self.birthdate.strftime("%Y-%m-%d")
        d["age"] = self.age()
        return d
