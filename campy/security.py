# coding: utf-8
from functools import wraps
from google.appengine.api import users
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound


class _Roles(object):
    SYSTEM_ADMINISTRATOR = "system administrator"
    ADVISOR = "advisor"
roles = _Roles


class UnauthorizedException(Exception):
    pass


def _get_roles(email):
    test_users = [
        "test@example.com",
        "augustodamario@gmail.com",
        "julio.veronelli@crossknight.com.ar",
        "magoarcano@gmail.com"]
    if email in test_users:
        return [roles.ADVISOR]
    return []


def get_current_user_roles():
    user = users.get_current_user()
    if user:
        r = _get_roles(user.email())
        if users.is_current_user_admin():
            r.append(roles.SYSTEM_ADMINISTRATOR)
        return r
    return []


def require_login(f):
    @wraps(f)
    def wrapper(request):
        if not users.get_current_user():
            raise HTTPFound(location=users.create_login_url(request.url))
        return f(request)
    return wrapper


def require_any_role(f):
    @wraps(f)
    def wrapper(request):
        if get_current_user_roles():
            return f(request)
        raise UnauthorizedException
    return wrapper


def require_role(*names):
    def decorator(f):
        @wraps(f)
        def wrapper(request):
            u_roles = get_current_user_roles()
            for name in names:
                if name in u_roles:
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
