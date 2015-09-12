# coding: utf-8
from functools import wraps
from google.appengine.api import users


class _Roles:
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


def has_current_user_role(name):
    user = users.get_current_user()
    return user and name in _get_roles(user.email())


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


def handle_exception(f):
    @wraps(f)
    def wrapper(ex, request):
        return _add_logout_url(f(ex, request))
    return wrapper
