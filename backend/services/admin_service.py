# services/admin_service.py

from firebase_admin import auth
from werkzeug.exceptions import NotFound, BadRequest

class AdminService:

    @staticmethod
    def list_users():
        users = []
        page = auth.list_users()

        for user in page.users:
            users.append({
                "uid": user.uid,
                "email": user.email,
                "disabled": user.disabled,
                "roles": user.custom_claims or {}
            })

        return users

    @staticmethod
    def delete_user(uid):
        try:
            auth.delete_user(uid)
        except auth.UserNotFoundError:
            raise NotFound("User not found")

    @staticmethod
    def assign_role(uid, role):
        if not uid or not role:
            raise BadRequest("Missing uid or role")
        
        current_claims = auth.get_user(uid).custom_claims or {}
        current_claims[role] = True

        auth.set_custom_user_claims(uid, current_claims)
        return {"uid": uid, "roles": current_claims}
