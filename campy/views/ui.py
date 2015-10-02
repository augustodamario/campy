# coding: utf-8
from campy.models import NATIONALITIES
from campy.security import require_any_role
from campy.security import require_login
from campy.security import UnauthorizedException
from google.appengine.api import users
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config


def includeme(config):
    config.add_route("home", "/", request_method="GET")
    config.add_route("templates", "/templates/{name}.html", request_method="GET")
    config.add_route("logout", "/salir", request_method="GET")
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
    context = {"nationalities": NATIONALITIES}
    return Response(render(request.matchdict["name"] + ".html", context, request=request))


@view_config(route_name="logout")
def logout(request):
    return HTTPFound(location=users.create_logout_url("/"))
