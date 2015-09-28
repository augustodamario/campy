# coding: utf-8
from datetime import date
from datetime import datetime
from google.appengine.ext.ndb import DateProperty
from google.appengine.ext.ndb import DateTimeProperty
from google.appengine.ext.ndb import Model
from google.appengine.ext.ndb import StringProperty
from google.appengine.ext.ndb import TextProperty


class BaseModel(Model):
    def json(self, include=None, exclude=None):
        d = super(BaseModel, self).to_dict(include=include, exclude=exclude)
        for k, v in d.iteritems():
            if isinstance(v, datetime):
                d[k] = v.strftime("%Y-%m-%dT%H:%M:%SZ")
            elif isinstance(v, date):
                d[k] = v.strftime("%Y-%m-%d")
        d["id"] = self.key.id()
        return d


class Patient(BaseModel):
    createdon = DateTimeProperty(required=True, indexed=False, auto_now_add=True)
    modifiedon = DateTimeProperty(required=True, auto_now=True)
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
            today = date.today()
            years = today.year - self.birthdate.year - 1
            if today.month > self.birthdate.month or\
                    (today.month == self.birthdate.month and today.day >= self.birthdate.day):
                years += 1
            return max(0, years)
        return None

    def json(self, include=None, exclude=None):
        d = super(Patient, self).json(include=include, exclude=exclude)
        d["age"] = self.age()
        return d
