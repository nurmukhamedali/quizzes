# tests/test_question.py

import requests
import pytest

created_questions = []

def test_create_questions(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Use existing topics or mock topic IDs
    topic_ids = ["topic_123", "topic_456"]  # Replace with your actual test topics

    for i, topic_id in enumerate(topic_ids, start=1):
        payload = {
            "topic_id": topic_id,
            "number": i,
            "text": f"What is question {i}?",
            "type": "radio",
            "options": [{"id": "A", "text": "Option A"}, {"id": "B", "text": "Option B"}],
            "correct_answers": ["A"]
        }
        rv = requests.post(f"{base_url}/questions/", json=payload, headers=headers)
        assert rv.status_code == 201
        data = rv.json()
        created_questions.append(data["id"])

def test_get_question_by_id(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    for question_id in created_questions:
        rv = requests.get(f"{base_url}/questions/{question_id}", headers=headers)
        assert rv.status_code == 200
        data = rv.json()
        assert data["id"] == question_id

def test_list_questions(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    rv = requests.get(f"{base_url}/questions/", headers=headers)
    assert rv.status_code == 200
    data = rv.json()
    assert "questions" in data

def test_filter_questions_by_topic(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    topic_id = "topic_123"
    rv = requests.get(f"{base_url}/questions/?topic_id={topic_id}", headers=headers)
    assert rv.status_code == 200
    data = rv.json()
    for q in data["questions"]:
        assert q["topic_id"] == topic_id

def test_update_questions(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    for question_id in created_questions:
        payload = {
            "topic_id": "topic_123",
            "number": 1,
            "text": "Updated question text",
            "type": "radio",
            "options": [{"id": "A", "text": "Updated Option"}],
            "correct_answers": ["A"]
        }
        rv = requests.put(f"{base_url}/questions/{question_id}", json=payload, headers=headers)
        assert rv.status_code == 200

def test_delete_questions(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    for question_id in created_questions:
        rv = requests.delete(f"{base_url}/questions/{question_id}", headers=headers)
        assert rv.status_code == 200
