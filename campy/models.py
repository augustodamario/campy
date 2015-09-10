# coding: utf-8
from google.appengine.ext.ndb import DateProperty
from google.appengine.ext.ndb import Model
from google.appengine.ext.ndb import StringProperty
from google.appengine.ext.ndb import TextProperty


class Patient(Model):
    firstname = StringProperty(required=True)
    middlename = StringProperty()
    surname = StringProperty()
    birthdate = DateProperty(required=True, indexed=False)
    nationality = StringProperty(indexed=False)
    cellphone = StringProperty()
    email = StringProperty()
    notes = TextProperty()
