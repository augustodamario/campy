# coding: utf-8
from google.appengine.api import users
from google.appengine.ext.ndb import Key
from models import Patient
from security import get_current_user_roles
from security import handle_rest
from security import require_any_role
from security import require_login
from security import UnauthorizedException
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config
from validators import PatientForm


def includeme(config):
    config.add_route("home", "/", request_method="GET")
    config.add_route("templates", "/templates/{name}.html", request_method="GET")
    config.add_route("logout", "/salir", request_method="GET")
    config.add_route("api-user-current", "/api/user", request_method="GET")
    config.add_route("api-patient-new", "/api/patient", request_method="POST")
    config.add_route("api-patient", "/api/patient/{id}", request_method="GET")
    config.add_route("api-patients-last", "/api/patients/last", request_method="GET")
    config.scan(__name__)


@view_config(context=UnauthorizedException, renderer="unauthorized.html")
def unauthorized(ex, request):
    return {}


@view_config(route_name="home", renderer="index.html")
@require_login
def home(request):
    return {}


@view_config(route_name="templates")
@require_any_role
def templates(request):
    return Response(render(request.matchdict["name"] + ".html", {}, request=request))


@view_config(route_name="logout")
def logout(request):
    return HTTPFound(location=users.create_logout_url("/"))


@view_config(route_name="api-user-current", renderer="json")
@handle_rest
@require_any_role
def api_user_current(request):
    return {
        "user": users.get_current_user().email(),
        "roles": get_current_user_roles()
    }


@view_config(route_name="api-patient-new", renderer="json")
@handle_rest
@require_any_role
def api_patient_new(request):
    form = PatientForm(data=request.json_body)
    if form.validate():
        patient = Patient()
        form.populate_obj(patient)
        key = patient.put()
        return {"id": key.id()}
    else:
        raise HTTPBadRequest(json=form.errors)


@view_config(route_name="api-patient", renderer="json")
@handle_rest
@require_any_role
def api_patient(request):
    try:
        pid = int(request.matchdict["id"])
    except ValueError:
        raise HTTPBadRequest(json={})
    patient = Key(Patient, pid).get()
    if not patient:
        raise HTTPNotFound(json={})
    return patient.json()


@view_config(route_name="api-patients-last", renderer="json")
@handle_rest
@require_any_role
def api_patients_last(request):
    attributes = ["id", "modifiedon", "firstname", "surname", "birthdate", "age", "cellphone", "email"]
    return [p.json(include=attributes) for p in Patient.query().order(-Patient.modifiedon)]
