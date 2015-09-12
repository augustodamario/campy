# coding: utf-8
from security import handle_exception
from security import require_role
from security import roles
from security import UnauthorizedException
from pyramid.view import view_config


def includeme(config):
    config.add_route("home", "/")
    config.add_route("new_patient", "/paciente/nuevo")
    config.scan(__name__)


@view_config(context=UnauthorizedException, renderer="unauthorized.html")
@handle_exception
def unauthorized(ex, request):
    return {}


@view_config(route_name="home", renderer="home.html")
@require_role(roles.ADVISOR)
def home(request):
    return {}


@view_config(route_name="new_patient", renderer="patient/new.html")
@require_role(roles.ADVISOR)
def new_patient(request):
    return {}
