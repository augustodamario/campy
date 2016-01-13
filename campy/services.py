# coding: utf-8
from campy.models import Patient
from campy.models import User
from campy.security import roles
from google.appengine.ext.ndb import Key


def list_users(branch, role=roles.ADVISOR):
    return User.query(User.roles == role, ancestor=branch.key).fetch()


def get_patient(branch, pid):
    return Key(Patient, pid, parent=branch.key).get()


def list_last_patients(branch):
    return Patient.query(ancestor=branch.key).order(-Patient.modifiedon).fetch()
