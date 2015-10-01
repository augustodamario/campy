# coding: utf-8
from functools import wraps
from google.appengine.api import users
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
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


# Pyramid tween factory: sets user session data on each request
def session_tween_factory(handler, registry):
    test_users = [
        "test@example.com",
        "augustodamario@gmail.com",
        "julio.veronelli@crossknight.com.ar",
        "magoarcano@gmail.com"]

    def session_tween(request):
        _user = None
        g_user = users.get_current_user()
        if g_user:
            _email = g_user.email()
            _roles = []
            if users.is_current_user_admin():
                _roles.append(roles.SYSTEM_ADMINISTRATOR)
            if _email in test_users:
                _roles.append(roles.ADVISOR)
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
