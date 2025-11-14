# tests/test_error_handling.py
import requests
import pytest

def test_unauthorized_no_token(base_url):
    """No Authorization header"""
    rv = requests.get(f"{base_url}/topics/")
    assert rv.status_code == 401
    

def test_unauthorized_invalid_token(base_url):
    """Invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    rv = requests.get(f"{base_url}/topics/", headers=headers)
    assert rv.status_code == 401
    

def test_forbidden_user_token(base_url, user_token):
    """Normal user trying to create topic (admin only)"""
    headers = {"Authorization": f"Bearer {user_token}", "Content-Type": "application/json"}
    payload = {"name": "Forbidden Topic"}
    rv = requests.post(f"{base_url}/topics/", json=payload, headers=headers)
    assert rv.status_code == 403
    data = rv.json()
    assert "role required" in data.get("message", "").lower() or "FORBIDDEN" in data.get("error", "")

def test_not_found_topic(base_url, admin_token):
    """Accessing non-existent topic"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    rv = requests.get(f"{base_url}/topics/nonexistent_id", headers=headers)
    assert rv.status_code == 404
    data = rv.json()
    assert "not found" in data.get("message", "").lower() or "NOT_FOUND" in data.get("error", "")

def test_not_found_question(base_url, admin_token):
    """Accessing non-existent question"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    rv = requests.get(f"{base_url}/questions/nonexistent_id", headers=headers)
    assert rv.status_code == 404
    data = rv.json()
    assert "not found" in data.get("message", "").lower() or "NOT_FOUND" in data.get("error", "")

def test_validation_error_missing_field(base_url, admin_token):
    """POST missing required field 'name' in topic"""
    headers = {"Authorization": f"Bearer {admin_token}", "Content-Type": "application/json"}
    payload = {}  # missing 'name'
    rv = requests.post(f"{base_url}/topics/", json=payload, headers=headers)
    assert rv.status_code == 400
    data = rv.json()
    assert "validation_errors" in data or "VALIDATION_ERROR" in data.get("error", "")

def test_validation_error_invalid_option_id(base_url, admin_token):
    """POST question with invalid option id"""
    headers = {"Authorization": f"Bearer {admin_token}", "Content-Type": "application/json"}
    payload = {
        "topic_id": "topic_123",
        "number": 1,
        "text": "Test question",
        "type": "radio",
        "options": [{"id": "Z1", "text": "Invalid Option"}],  # invalid ID
        "correct_answers": ["Z1"]
    }
    rv = requests.post(f"{base_url}/questions/", json=payload, headers=headers)
    assert rv.status_code == 400
    data = rv.json()
    assert "validation_errors" in data or "VALIDATION_ERROR" in data.get("error", "")
