# tests/test_cards.py

import requests
import pytest

created_topic_id = None
created_questions = []
created_cards = []

def test_create_topics(base_url, admin_token):
    global created_topic_id

    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"name": "CardTopic", "description": "Topic for Card test"}

    rv = requests.post(f"{base_url}/topics/", json=payload, headers=headers)
    assert rv.status_code == 201

    data = rv.json()
    created_topic_id = data["id"]

    assert "id" in data
    assert created_topic_id is not None

def test_create_questions(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Use existing topics or mock topic IDs
    topic_id = created_topic_id # Replace with your actual test topics

    for i in range(1, 5):
        payload = {
            "topic_id": topic_id,
            "number": i,
            "text": f"Card Test: What is Question {i}?",
            "type": "radio",
            "options": [{"id": "A", "text": "Option A"}, {"id": "B", "text": "Option B"}],
            "correct_answers": ["A"]
        }

        rv = requests.post(f"{base_url}/questions/", json=payload, headers=headers)
        assert rv.status_code == 201

        data = rv.json()
        created_questions.append(data["id"])

        assert "id" in data

# Create Cards (user_token)
def test_create_cards(base_url, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    for qid in created_questions:
        payload = {"question_id": qid}
        rv = requests.post(f"{base_url}/cards/", json=payload, headers=headers)
        print(rv.content)
        assert rv.status_code == 201
        data = rv.json()

        created_cards.append(data["id"])
        assert "id" in data

# Prevent Duplicate Cards
def test_prevent_duplicate_cards(base_url, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    # Try creating a card again for the same question
    payload = {"question_id": created_questions[0]}
    rv = requests.post(f"{base_url}/cards/", json=payload, headers=headers)

    assert rv.status_code == 400  # BadRequest expected

# List Cards by Topic (user-specific)
def test_list_cards_by_topic(base_url, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    rv = requests.get(f"{base_url}/cards/?topic_id={created_topic_id}", headers=headers)
    assert rv.status_code == 200

    data = rv.json()
    assert "cards" in data

    for card in data["cards"]:
        assert card["topic_id"] == created_topic_id

# Get Card by ID
def test_get_card_by_id(base_url, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    for cid in created_cards:
        rv = requests.get(f"{base_url}/cards/{cid}", headers=headers)
        assert rv.status_code == 200
        data = rv.json()

        assert data["id"] == cid

# Review Card (update spaced repetition data)
def test_review_card(base_url, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    for cid in created_cards:
        payload = {"is_correct": True}
        rv = requests.post(f"{base_url}/cards/{cid}/review", json=payload, headers=headers)

        assert rv.status_code == 200
        data = rv.json()

        assert data["id"] == cid
        assert "interval" in data
        assert "ease_factor" in data
        assert "next_review" in data

# Delete Cards
def test_delete_cards(base_url, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    for cid in created_cards:
        rv = requests.delete(f"{base_url}/cards/{cid}", headers=headers)
        assert rv.status_code == 200

# Delete Topic (should cascade delete questions)
def test_delete_topic_after_cards(base_url, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    rv = requests.delete(f"{base_url}/topics/{created_topic_id}", headers=headers)
    assert rv.status_code == 200