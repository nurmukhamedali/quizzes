from flask import Blueprint, request, jsonify, g
from auth.firebase_auth import verify_firebase_token, set_user_role, has_admin_role
from middleware.auth_decorators import require_auth, require_role

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/profile', methods=['GET'])
@require_auth
def profile():
    user = g.user  # user info injected by decorator
    return jsonify({
        "message": "Authenticated user.",
        "uid": user["uid"],
        "email": user.get("email")
    })

@auth_bp.route('/admin', methods=['GET'])
@require_role('admin')
def admin_route():
    user = g.user
    return jsonify({"message": "Welcome, admin!", "email": user.get("email")})


@auth_bp.route('/set-role', methods=['POST'])
@require_role('admin')  # only admin users can assign roles (you can restrict further)
def assign_role():
    data = request.get_json()
    uid = data.get("uid")
    role = data.get("role")
    if not uid or not role:
        return jsonify({"error": "Missing uid or role"}), 400

    try:
        set_user_role(uid, role)
        return jsonify({"message": f"Role '{role}' added to {uid}."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
