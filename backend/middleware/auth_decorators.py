# middleware/auth_decorators.py

from functools import wraps
from flask import request, jsonify, g
from auth.firebase_auth import verify_firebase_token
from werkzeug.exceptions import Unauthorized, Forbidden

def require_auth(f):
    """Decorator to ensure the request has a valid Firebase ID token."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user, error = verify_firebase_token(request)

        # Raise a built-in Flask/Werkzeug exception
        if error:
            return Unauthorized(description=error)  
        
        # store the user in flask.g (global request context)
        g.user = user
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(role_name):
    """Decorator to ensure the user has a specific custom claim (e.g., admin=True)."""
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user, error = verify_firebase_token(request)

            # Raise a built-in Flask/Werkzeug exception
            if error:
                raise Unauthorized(description=error)

            if not user.get(role_name):
                raise Forbidden(description=f"{role_name.title()} role required")

            g.user = user
            return f(*args, **kwargs)
        
        return decorated_function
    return wrapper
