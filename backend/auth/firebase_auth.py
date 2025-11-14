from firebase_admin import auth

def verify_firebase_token(request):
    """
    Extract and verify Firebase ID token from Authorization header.
    Expected format: Authorization: Bearer <token>
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None, "Missing Authorization header"
    try:
        token = auth_header.split("Bearer ")[-1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token, None
    except Exception as e:
        return None, str(e)

