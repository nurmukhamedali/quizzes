# controllers/admin_controller.py

from flask import jsonify
from services.admin_service import AdminService

class AdminController:

    @staticmethod
    def dashboard(user):
        return jsonify({"message": "Welcome, admin!", "email": user.get("email")})

    @staticmethod
    def list_users():
        users = AdminService.list_users()
        return jsonify({"users": users})

    @staticmethod
    def delete_user(uid):
        AdminService.delete_user(uid)
        return jsonify({"deleted": uid})

    @staticmethod
    def assign_role(data):
        uid, roles = AdminService.assign_role(data.get("uid"), data.get("role"))
        return jsonify({
            "message": f"Role '{data.get('role')}' set for {uid}",
            "roles": roles
        })
