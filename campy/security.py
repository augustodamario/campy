# coding: utf-8
from functools import wraps
from google.appengine.api import users
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound


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
        user = users.get_current_user()
        if user:
            _email = user.email()
            _roles = []
            if users.is_current_user_admin():
                _roles.append(roles.SYSTEM_ADMINISTRATOR)
            if _email in test_users:
                _roles.append(roles.ADVISOR)
            request.user = _User(_email, _roles)
        else:
            request.user = None
        return handler(request)
    return session_tween


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
