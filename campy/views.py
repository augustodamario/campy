# coding: utf-8
from pyramid.view import view_config


def includeme(config):
    config.add_route("home", "/")
    config.add_route("new_patient", "/paciente/nuevo")
    config.scan(__name__)


@view_config(route_name="home", renderer="home.html")
def home(request):
    return {}


@view_config(route_name="new_patient", renderer="patient/new.html")
def new_patient(request):
    return {}
