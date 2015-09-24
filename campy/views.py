# coding: utf-8
from google.appengine.api import users
from security import get_current_user_roles
from security import handle_rest
from security import require_any_role
from security import require_login
from security import UnauthorizedException
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config


def includeme(config):
    config.add_route("home", "/")
    config.add_route("templates", "/templates/{name}.html")
    config.add_route("logout", "/salir")
    config.add_route("api-user-current", "/api/user/CURRENT")
    config.add_route("api-patients-last", "/api/patients/last")
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
    user = users.get_current_user()
    return {
        "user": user.email() if user else None,
        "roles": get_current_user_roles()
    }


@view_config(route_name="api-patients-last", renderer="json")
@handle_rest
@require_any_role
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
