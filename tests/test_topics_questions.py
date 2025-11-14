# tests/test_topic.py

import requests
import pytest

created_topics = []

def test_create_topics(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payloads = [
        {"name": "Math", "description": "Math topics"},
        {"name": "Science", "description": "Science topics"}
    ]

    for payload in payloads:
        rv = requests.post(f"{base_url}/topics/", json=payload, headers=headers)
        assert rv.status_code == 201
        data = rv.json()
        created_topics.append(data["id"])
        assert "id" in data

def test_get_topic_by_id(base_url, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    for topic_id in created_topics:
        rv = requests.get(f"{base_url}/topics/{topic_id}", headers=headers)
        assert rv.status_code == 200
        data = rv.json()
        assert data["id"] == topic_id

def test_list_topics(base_url, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    rv = requests.get(f"{base_url}/topics/", headers=headers)
    assert rv.status_code == 200
    data = rv.json()
    assert "topics" in data
    assert all("id" in t for t in data["topics"])

def test_update_topics(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    for topic_id in created_topics:
        payload = {"name": "Updated Topic", "description": "Updated description"}
        rv = requests.put(f"{base_url}/topics/{topic_id}", json=payload, headers=headers)
        assert rv.status_code == 200


created_questions = []

def test_create_questions(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Use existing topics or mock topic IDs
    topic_ids = created_topics # Replace with your actual test topics

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
    for topic_id in created_topics:
        rv = requests.get(f"{base_url}/questions/?topic_id={topic_id}", headers=headers)
        assert rv.status_code == 200
        data = rv.json()
        for q in data["questions"]:
            assert q["topic_id"] == topic_id

def test_update_questions(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    number = 8000
    for question_id in created_questions:
        payload = {
            "topic_id": created_topics[0],
            "number": number,
            "text": "Updated question text",
            "type": "radio",
            "options": [{"id": "A", "text": "Updated Option"}],
            "correct_answers": ["A"]
        }
        number += 1
        rv = requests.put(f"{base_url}/questions/{question_id}", json=payload, headers=headers)
        print(rv.content)
        assert rv.status_code == 200

def test_delete_questions(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    for question_id in created_questions:
        rv = requests.delete(f"{base_url}/questions/{question_id}", headers=headers)
        assert rv.status_code == 200

def test_delete_topics(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    for topic_id in created_topics:
        rv = requests.delete(f"{base_url}/topics/{topic_id}", headers=headers)
        assert rv.status_code == 200
