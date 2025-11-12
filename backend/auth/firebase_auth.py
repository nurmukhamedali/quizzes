from firebase_admin import auth

def verify_firebase_token(request):
    """Extract and verify Firebase ID token from Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None, "Missing Authorization header"
    try:
        token = auth_header.split("Bearer ")[-1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token, None
    except Exception as e:
        return None, str(e)

def set_user_role(uid, role):
    """Assign custom role claim (e.g., admin=True)."""
    auth.set_custom_user_claims(uid, {role: True})
    
    return auth.get_user(uid)

def has_admin_role(uid):
    claims = auth.get_user(uid).custom_claims
    return claims.get("admin")