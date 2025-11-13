from flask import Blueprint, jsonify, g
from middleware.auth_decorators import require_auth, require_role

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/profile', methods=['GET'])
@require_auth
def profile():
    user = g.user  # user info injected by decorator
    return jsonify({
        "uid": user["uid"],
        "email": user.get("email"),
        "message": "This is your profile data."
    })

