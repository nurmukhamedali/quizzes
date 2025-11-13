from flask import Blueprint, request, jsonify, g
from auth.firebase_auth import set_user_role
from middleware.auth_decorators import require_role

admin_bp = Blueprint('admin', __name__)

# Admin Main Route 
@admin_bp.route('/', methods=['GET'])
@require_role('admin')
def admin_route():
    user = g.user
    return jsonify({"message": "Welcome, admin!", "email": user.get("email")})

# List Users
@admin_bp.route('/users', methods=['GET'])
@require_role('admin')
def list_users():
    """Admin-only route to list all users (dummy data for now)."""
    dummy_users = [
        {"uid": "u1", "email": "user1@example.com"},
        {"uid": "u2", "email": "user2@example.com"}
    ]
    return jsonify(dummy_users)

# DELETE a user
@admin_bp.route('/users/<uid>', methods=['DELETE'])
@require_role('admin')
def delete_user(uid):
    # placeholder example — integrate with your DB later
    return jsonify({"message": f"User {uid} deleted successfully"})

# SET Role
@admin_bp.route('/role', methods=['POST'])
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


