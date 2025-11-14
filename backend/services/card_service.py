# services/card_service.py

from config.settings import db
from werkzeug.exceptions import NotFound, BadRequest
from datetime import datetime, timedelta, timezone

cards_ref = db.collection("cards")
questions_ref = db.collection("questions")
topics_ref = db.collection("topics")

class CardService:

    @staticmethod
    def list(user_id, topic_id):
        """List cards for a specific user and topic."""

        if not user_id:
            raise BadRequest("user_id is required")
        if not topic_id:
            raise BadRequest("topic_id is required")

        query = (
            cards_ref
            .where("user_id", "==", user_id)
            .where("topic_id", "==", topic_id)
        )

        return [ dict(doc.to_dict(), id=doc.id) for doc in query.stream() ]

    @staticmethod
    def get(card_id):
        ref = cards_ref.document(card_id)
        doc = ref.get()
        if not doc.exists:
            raise NotFound("Card not found")
        
        return dict(doc.to_dict(), id=doc.id)

    @staticmethod
    def create(user_id, question_id):
        # Ensure question exists
        qdoc = questions_ref.document(question_id).get()
        if not qdoc.exists:
            raise NotFound("Question not found")

        question = qdoc.to_dict()
        topic_id = question["topic_id"]

        # Ensure card does NOT already exist for this user & question
        existing = (
            cards_ref
            .where("user_id", "==", user_id)                
            .where("question_id", "==", question_id)
            .limit(1)
        ).stream()
        
        if any(existing):
            raise BadRequest("Card for this question already exists for this user")

        card_data = {
            "user_id": user_id,
            "question_id": question_id,
            "topic_id": topic_id,

            # spaced repetition fields
            "ease_factor": 2.5,
            "interval": 1,
            "repetitions": 0,
            "correct_answered_count": 0,
            "next_review": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),

            "createdAt": datetime.now(timezone.utc).isoformat()
        }

        ref = cards_ref.document()
        ref.set(card_data)

        return {**card_data, "id": ref.id}

    @staticmethod
    def update_after_answer(card_id, is_correct: bool):
        ref = cards_ref.document(card_id)
        doc = ref.get()

        if not doc.exists:
            raise NotFound("Card not found")

        data = doc.to_dict()

        ease = data["ease_factor"]
        interval = data["interval"]
        reps = data["repetitions"]

        if is_correct:
            reps += 1
            data["correct_answered_count"] += 1
            ease += 0.1

            if reps == 1:
                interval = 1
            else:
                interval = int(interval * ease)

        else:
            reps = 0
            ease = max(1.3, ease - 0.2)
            interval = 1  # reset

        next_review_date = datetime.now(timezone.utc) + timedelta(days=interval)

        data.update({
            "ease_factor": ease,
            "interval": interval,
            "repetitions": reps,
            "next_review": next_review_date.isoformat(),
            "correct_answered_count": data["correct_answered_count"]
        })

        ref.update(data)

        return {**data, "id": card_id}

    @staticmethod
    def delete(card_id):
        ref = cards_ref.document(card_id)
        if not ref.get().exists:
            raise NotFound("Card not found")
        
        ref.delete()

        return card_id
