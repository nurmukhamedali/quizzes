# services/question_service.py

from config.settings import db
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime

questions_ref = db.collection("questions")
topics_ref = db.collection("topics")

class QuestionService:
    @staticmethod
    def list(topic_id=None):
        """List all questions, optionally filter by topic_id"""
        query = questions_ref
        if topic_id:
            query = query.where("topic_id", "==", topic_id)

        return [dict(doc.to_dict(), id=doc.id) for doc in query.stream()]
    
    @staticmethod
    def get(question_id):
        ref = questions_ref.document(question_id)
        doc = ref.get()
        if not doc.exists:
            raise NotFound(description=f"Question {question_id} not found")
        return dict(doc.to_dict(), id=doc.id)

    @staticmethod
    def create(data, user_id):
        QuestionService.validate_business_rules(data)

        topic_id = data["topic_id"]

        # Ensure topic exists
        topic = topics_ref.document(topic_id).get()
        if not topic.exists:
            raise NotFound("Topic not found")
        
        # Ensure unique number within this topic
        QuestionService.ensure_unique_number(topic_id, data["number"])

        data.update({
            "createdBy": user_id,
            "createdAt": datetime.now().isoformat()
        })

        ref = questions_ref.document()
        ref.set(data)

        return {**data, "id": ref.id}

    @staticmethod
    def update(question_id, data):
        QuestionService.validate_business_rules(data)

        # Ensure question exists
        ref = questions_ref.document(question_id)
        if not ref.get().exists:
            raise NotFound(description="Question not found")
        
        topic_id = data["topic_id"]

        # Ensure topic exists
        topic = topics_ref.document(topic_id).get()
        if not topic.exists:
            raise NotFound("Topic not found")
        
        # Ensure unique number (excluding current id)
        QuestionService.ensure_unique_number(topic_id, data["number"], exclude_id=question_id)
        
        ref.update(data)

        return {**data, "id": question_id}

    @staticmethod
    def delete(question_id):
        ref = questions_ref.document(question_id)
        if not ref.get().exists:
            raise NotFound(description="Question not found")
        
        ref.delete()

        return question_id
    
    @staticmethod
    def delete_questions_for_topic(topic_id):
        """Cascade delete when topic is removed."""
        qs = questions_ref.where("topic_id", "==", topic_id).stream()
        for q in qs:
            q.reference.delete()

    @staticmethod
    def validate_business_rules(data):
        q_type = data.get("type")
        options = data.get("options")
        correct = data.get("correct_answers", [])

        # Rule 1: radio / checkbox must have options
        if q_type in ["radio", "checkbox"] and (not options or len(options) == 0):
            raise BadRequest(description=f"{q_type} questions must include options")

        # Rule 2: input must NOT have options
        if q_type == "input" and options:
            raise BadRequest(description="input questions must not include options")

        # Rule 3: radio must have exactly 1 correct answer
        if q_type == "radio" and len(correct) != 1:
            raise BadRequest(description="radio questions must have exactly one correct answer")

        # Rule 4: checkbox/input must have at least one correct answer
        if q_type in ["checkbox", "input"] and len(correct) < 1:
            raise BadRequest(description=f"{q_type} questions must have at least one correct answer")

    @staticmethod
    def ensure_unique_number(topic_id, number, exclude_id=None):
        """Ensure that no other question in this topic has the same number."""

        query = (
            questions_ref
            .where("topic_id", "==", topic_id)
            .where("number", "==", number)
        )

        for doc in query.stream():
            if exclude_id and doc.id == exclude_id:
                continue
            raise BadRequest(f"Question number '{number}' already exists in this topic.")