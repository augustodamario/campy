# coding: utf-8
from campy.models import Branch
from campy.models import User
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
    def __init__(self, a_email, a_roles):
        self.email = a_email
        self.roles = a_roles


class _Roles(object):
    SYSTEM_ADMINISTRATOR = "system administrator"
    ADVISOR = "advisor"
roles = _Roles


class UnauthorizedException(Exception):
    pass


# Pyramid tween factory: sets user session and branch data on each request
def session_tween_factory(handler, registry):
    branch_prefix = "/sede/([a-z]+)/.*"

    def session_tween(request):
        _branch = None
        m = match(branch_prefix, request.path)
        if m:
            _branch = m.group(1)
            if not Key(Branch, _branch).get():
                return HTTPNotFound()
        request.branch = _session.branch = _branch

        _user = None
        g_user = users.get_current_user()
        if g_user:
            _email = g_user.email()
            _roles = []
            if users.is_current_user_admin():
                _roles.append(roles.SYSTEM_ADMINISTRATOR)
            if _branch:
                c_user = Key(Branch, _branch, User, _email).get()
                if c_user:
                    _roles.extend(c_user.roles)
            _user = _User(_email, _roles)
        request.user = _session.user = _user
        return handler(request)
    return session_tween


def get_current_user():
    return _session.user


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
