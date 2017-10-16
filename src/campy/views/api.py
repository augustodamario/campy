# coding: utf-8
from campy.models import Patient
from campy.models import roles
from campy.security import handle_rest
from campy.security import require_any_role
from campy.security import require_role
from campy.security import UnauthorizedException
from campy.services import get_patient
from campy.services import list_last_patients
from campy.services import list_users
from campy.validation.forms import PatientForm
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config


def includeme(config):
    config.add_route("api-user-current", "/user", request_method="GET")
    config.add_route("api-users-advisors", "/users/advisors", request_method="GET")
    config.add_route("api-patient-new", "/patient", request_method="POST")
    config.add_route("api-patient", "/patient/{id:[0-9]+}", request_method="GET")
    config.add_route("api-patient-edit", "/patient/{id:[0-9]+}", request_method="POST")
    config.add_route("api-patients-last", "/patients/last", request_method="GET")
    config.scan(__name__)


@view_config(route_name="api-user-current", renderer="json")
@handle_rest
@require_any_role
def api_user_current(request):
    return request.user.json()


@view_config(route_name="api-users-advisors", renderer="json")
@handle_rest
@require_any_role
def api_users_advisors(request):
    return [u.json(include=["id", "name"]) for u in list_users(request.branch, roles.ADVISOR)]


@view_config(route_name="api-patient-new", renderer="json")
@handle_rest
@require_role(roles.SYSTEM_ADMINISTRATOR, roles.SECRETARY)
def api_patient_new(request):
    form = PatientForm(data=request.json_body)
    if not form.validate():
        raise HTTPBadRequest(json=form.errors)
    patient = Patient(parent=request.branch.key)
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
    patient = get_patient(request.branch, pid)
    if not patient:
        raise HTTPNotFound(json={})
    rs = request.user.roles
    if roles.SYSTEM_ADMINISTRATOR not in rs and roles.SECRETARY not in rs and not patient.has_advisor(request.user):
        raise UnauthorizedException
    return patient.json()


@view_config(route_name="api-patient-edit", renderer="json")
@handle_rest
@require_any_role
def api_patient_edit(request):
    form = PatientForm(data=request.json_body)
    if not form.validate():
        raise HTTPBadRequest(json=form.errors)
    try:
        pid = int(request.matchdict["id"])
    except ValueError:
        raise HTTPBadRequest(json={})
    patient = get_patient(request.branch, pid)
    if not patient:
        raise HTTPNotFound(json={})
    rs = request.user.roles
    if roles.SYSTEM_ADMINISTRATOR not in rs and roles.SECRETARY not in rs and not patient.has_advisor(request.user):
        raise UnauthorizedException
    form.populate_obj(patient)
    key = patient.put()
    return {"id": key.id()}


@view_config(route_name="api-patients-last", renderer="json")
@handle_rest
@require_any_role
def api_patients_last(request):
    uroles = request.user.roles
    if roles.SYSTEM_ADMINISTRATOR in uroles or roles.SECRETARY in uroles:
        advisor = None
    elif roles.ADVISOR in uroles:
        advisor = request.user
    else:
        return []
    attributes = ["id", "modifiedon", "record", "firstname", "surname", "cellphone", "email"]
    return [p.json(include=attributes) for p in list_last_patients(request.branch, advisor)]
