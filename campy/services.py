# coding: utf-8
from campy.models import Patient
from campy.models import User
from google.appengine.ext.ndb import Key
from google.appengine.ext.ndb import OR


def get_user(branch, uid):
    return Key(User, uid, parent=branch.key).get()


def list_users(branch, role):
    users = User.query(User.roles == role, ancestor=branch.key).fetch()
    users.sort(key=lambda u: u.name.lower())
    return users


def get_patient(branch, pid):
    return Key(Patient, pid, parent=branch.key).get()


def list_last_patients(branch, advisor=None):
    if advisor is None:
        query = Patient.query(ancestor=branch.key)
    else:
        query = Patient.query(OR(Patient.advisor.id == advisor.id(), Patient.coadvisors.id == advisor.id()),
                              ancestor=branch.key)
    return query.order(-Patient.modifiedon).fetch()
