from functools import wraps
from flask import request, jsonify, g
from auth.firebase_auth import verify_firebase_token

def require_auth(f):
    """Decorator to ensure the request has a valid Firebase ID token."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user, error = verify_firebase_token(request)
        if error:
            return jsonify({"error": "Unauthorized", "details": error}), 401
        
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
            if error:
                return jsonify({"error": "Unauthorized", "details": error}), 401

            if not user.get(role_name):
                return jsonify({"error": f"Forbidden: {role_name.title()} role required"}), 403

            g.user = user
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
