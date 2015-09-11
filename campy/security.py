# coding: utf-8
from functools import wraps
from google.appengine.api import users


class Roles:
    ADVISOR = "advisor"
roles = Roles


class UnauthorizedException(Exception):
    pass


def get_roles(email):
    if email in ["test@example.com", "julio.veronelli@crossknight.com.ar"]:
        return [roles.ADVISOR]
    return []


def has_current_user_role(name):
    user = users.get_current_user()
    return user and name in get_roles(user.email())


def _add_logout_url(value):
    if isinstance(value, dict):
        value["logout_url"] = users.create_logout_url("/")
    return value


def require_role(*names):
    def decorator(f):
        @wraps(f)
        def wrapper(request):
            for name in names:
                if has_current_user_role(name):
                    return _add_logout_url(f(request))
            raise UnauthorizedException
        return wrapper
    return decorator


def exception(f):
    @wraps(f)
    def wrapper(ex, request):
        return _add_logout_url(f(ex, request))
    return wrapper
