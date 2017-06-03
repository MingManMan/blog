from functools import wraps
from flask import g,current_app
from .errors import forbidden


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.currnet_user.can(permission):
                return forbidden('Insufficient permissions')
            # current_app.logger.info(g.currnet_user)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
