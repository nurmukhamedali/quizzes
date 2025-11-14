# routes/admin_routes.py

from flask import Blueprint, request, g
from middleware.auth_decorators import require_role
from controllers.admin_controller import AdminController

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
@require_role('admin')
def admin_dashboard():
        return AdminController.dashboard(g.user)

@admin_bp.route('/users', methods=['GET'])
@require_role('admin')
def list_users():
        return AdminController.list_users()

@admin_bp.route('/users/<uid>', methods=['DELETE'])
@require_role('admin')
def delete_user(uid):
        return AdminController.delete_user(uid)

@admin_bp.route('/role', methods=['POST'])
@require_role('admin')
def assign_role():
        data = request.get_json()
        return AdminController.assign_role(data)
