# coding: utf-8
from security import add_logout_url
from security import handle_exception
from security import require_any_role
from security import UnauthorizedException
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config


def includeme(config):
    config.add_route("templates", "/templates/{name}.html")
    config.add_route("api-patients-last", "/api/patients/last")
    config.scan(__name__)


@view_config(context=UnauthorizedException, renderer="unauthorized.html")
@handle_exception
def unauthorized(ex, request):
    return {}


@view_config(route_name="templates")
@require_any_role
def templates(request):
    return Response(render(request.matchdict["name"] + ".html", add_logout_url({}), request=request))


@view_config(route_name="api-patients-last", renderer="json")
def api_patients_last(request):
    p1 = {
        "firstname": "Karen",
        "surname": "Rodríguez",
        "birthdate": "14 Mar 1977",
        "age": 38,
        "cellphone": "011 15 5567 3456",
        "email": "karen.suarez@gmail.com",
        "lastaccesseddate": "13/04/15",
        "lastaccessedtime": "14hs"
    }
    p2 = {
        "firstname": "Patricia",
        "surname": "Oliviera",
        "birthdate": "14 Jul 1983",
        "age": 29,
        "cellphone": "0322 15 5567 345",
        "email": "patri.oliviera@yahoo.com.ar",
        "lastaccesseddate": "13/04/15",
        "lastaccessedtime": "13hs"
    }
    return [p1, p2]
