# coding: utf-8
from campy.models import Branch
from campy.models import roles
from campy.models import User
from campy.security import require_login
from campy.security import require_role
from google.appengine.api import users
from google.appengine.ext.ndb import Key
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config


def includeme(config):
    config.add_route("root", "/", request_method="GET")
    config.add_route("logout", "/salir", request_method="GET")
    config.add_route("initialize", "/initialize", request_method="GET")
    config.scan(__name__)


@view_config(route_name="root")
@require_login
def root(request):
    return HTTPFound(location="/sede/caba/")


@view_config(route_name="logout")
def logout(request):
    return HTTPFound(location=users.create_logout_url("/"))


@view_config(route_name="initialize", renderer="string")
@require_role(roles.SYSTEM_ADMINISTRATOR)
def initialize(request):
    key = Key(Branch, "caba")
    if not key.get():
        Branch(key=key, name=u"Capital").put()
        u_roles = [roles.SECRETARY, roles.ADVISOR]
        User(parent=key, name=u"Juan Prueba", email="test@example.com", roles=u_roles).put()
        User(parent=key, name=u"Augusto D'Amario", email="augustodamario@gmail.com", roles=u_roles).put()
        User(parent=key, name=u"Julio Veronelli", email="julio.veronelli@crossknight.com.ar", roles=u_roles).put()
        User(parent=key, name=u"Hernán Acosta", email="magoarcano@gmail.com", roles=u_roles).put()
    return "OK"
