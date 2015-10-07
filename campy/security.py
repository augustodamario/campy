# coding: utf-8
from functools import wraps
from google.appengine.api import users
from google.appengine.ext.ndb import Key
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from re import match
import threading


_session = threading.local()


class _User(object):
    def __init__(self, a_name, a_email, a_roles):
        self.name = a_name
        self.email = a_email
        self.roles = a_roles

    def json(self):
        return {
            "name": self.name,
            "email": self.email,
            "roles": self.roles
        }


class _Roles(object):
    SYSTEM_ADMINISTRATOR = "system administrator"
    ADVISOR = "advisor"
roles = _Roles


class UnauthorizedException(Exception):
    pass


# Pyramid tween factory: sets current branch on each request
def branch_tween_factory(handler, registry):
    def tween(request):
        branch = None
        m = match("/sede/([a-z]+)/.*", request.path)
        if m:
            branch = Key("Branch", m.group(1)).get()
            if not branch:
                return HTTPNotFound()
        request.branch = _session.branch = branch
        return handler(request)
    return tween


def get_current_branch():
    return _session.branch if hasattr(_session, "branch") else None


# Pyramid tween factory: sets user session data on each request
def session_tween_factory(handler, registry):
    def tween(request):
        _user = None
        g_user = users.get_current_user()
        if g_user:
            _email = g_user.email()
            _roles = []
            _name = _email
            if users.is_current_user_admin():
                _roles.append(roles.SYSTEM_ADMINISTRATOR)
            if request.branch:
                c_user = Key("User", _email, parent=request.branch.key).get()
                if c_user:
                    _roles.extend(c_user.roles)
                    _name = c_user.name
            _user = _User(_name, _email, _roles)
        request.user = _session.user = _user
        return handler(request)
    return tween


def get_current_user():
    return _session.user if hasattr(_session, "user") else None


def require_login(f):
    @wraps(f)
    def wrapper(request):
        if not request.user:
            raise HTTPFound(location=users.create_login_url(request.url))
        return f(request)
    return wrapper


def require_any_role(f):
    @wraps(f)
    def wrapper(request):
        if request.user and request.user.roles:
            return f(request)
        raise UnauthorizedException
    return wrapper


def require_role(*names):
    def decorator(f):
        @wraps(f)
        def wrapper(request):
            if request.user and request.user.roles:
                for name in names:
                    if name in request.user.roles:
                        return f(request)
            raise UnauthorizedException
        return wrapper
    return decorator


def handle_rest(f):
    @wraps(f)
    def wrapper(request):
        try:
            return f(request)
        except UnauthorizedException:
            raise HTTPForbidden(json={})
    return wrapper
