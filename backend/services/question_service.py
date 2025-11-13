# services/question_service.py

from config.settings import db
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime

questions_ref = db.collection("questions")

class QuestionService:
    @staticmethod
    def list():
        return [dict(doc.to_dict(), id=doc.id) for doc in questions_ref.stream()]

    @staticmethod
    def create(data, user_id):
        QuestionService.validate_business_rules(data)
        data.update({
            "createdBy": user_id,
            "createdAt": datetime.now().isoformat()
        })
        _, ref = questions_ref.add(data)
        data["id"] = ref.id
        return data

    @staticmethod
    def update(question_id, data):
        QuestionService.validate_business_rules(data)
        ref = questions_ref.document(question_id)
        if not ref.get().exists:
            raise NotFound(description="Question not found")
        ref.update(data)
        return question_id

    @staticmethod
    def delete(question_id):
        ref = questions_ref.document(question_id)
        if not ref.get().exists:
            raise NotFound(description="Question not found")
        ref.delete()
        return question_id

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
