# coding: utf-8
from campy.models import Patient
from campy.security import handle_rest
from campy.security import require_any_role
from campy.validators import PatientForm
from google.appengine.ext.ndb import Key
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config


def includeme(config):
    config.add_route("api-user-current", "/user", request_method="GET")
    config.add_route("api-patient-new", "/patient", request_method="POST")
    config.add_route("api-patient", "/patient/{id:[0-9]+}", request_method="GET")
    config.add_route("api-patients-last", "/patients/last", request_method="GET")
    config.scan(__name__)


@view_config(route_name="api-user-current", renderer="json")
@handle_rest
@require_any_role
def api_user_current(request):
    return {
        "user": request.user.email,
        "roles": request.user.roles
    }


@view_config(route_name="api-patient-new", renderer="json")
@handle_rest
@require_any_role
def api_patient_new(request):
    form = PatientForm(data=request.json_body)
    if not form.validate():
        raise HTTPBadRequest(json=form.errors)
    patient = Patient()
    form.populate_obj(patient)
    key = patient.put()
    return {"id": key.id()}


@view_config(route_name="api-patient", renderer="json")
@handle_rest
@require_any_role
def api_patient(request):
    try:
        pid = int(request.matchdict["id"])
    except ValueError:
        raise HTTPBadRequest(json={})
    patient = Key(Patient, pid, parent=request.branch.key).get()
    if not patient:
        raise HTTPNotFound(json={})
    return patient.json()


@view_config(route_name="api-patients-last", renderer="json")
@handle_rest
@require_any_role
def api_patients_last(request):
    attributes = ["id", "modifiedon", "firstname", "surname", "birthdate", "age", "cellphone", "email"]
    return [p.json(include=attributes) for p in Patient.query(ancestor=request.branch.key).order(-Patient.modifiedon)]
