# tests/test_topics.py

import requests
import pytest

created_topics = []

def test_create_topics(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payloads = [
        {"name": "Topic 1", "description": "Topic for test"},
        {"name": "Topic 2", "description": "Topic for test"}
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

def test_delete_topics(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    for topic_id in created_topics:
        rv = requests.delete(f"{base_url}/topics/{topic_id}", headers=headers)
        assert rv.status_code == 200
