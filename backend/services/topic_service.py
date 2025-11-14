# services/topic_service.py

from config.settings import db
from werkzeug.exceptions import NotFound
from datetime import datetime, timezone
from services.question_service import QuestionService

topics_ref = db.collection("topics")

class TopicService:
    @staticmethod
    def list():
        return [ dict(doc.to_dict(), id=doc.id) for doc in topics_ref.stream() ]

    @staticmethod
    def get(topic_id):
        ref = topics_ref.document(topic_id)
        doc = ref.get()
        if not doc.exists:
            raise NotFound(description=f"Topic {topic_id} not found")
        return dict(doc.to_dict(), id=doc.id)

    @staticmethod
    def create(data, user_id):
        data.update({
            "createdBy": user_id,
            "createdAt": datetime.now(timezone.utc).isoformat()
        })

        ref = topics_ref.document()  # generate ID first
        ref.set(data)

        return {**data, "id": ref.id}

    @staticmethod
    def update(topic_id, data):
        ref = topics_ref.document(topic_id)
        if not ref.get().exists:
            raise NotFound(description="Topic not found")
        
        ref.update(data)

        return {**data, "id": topic_id}

    @staticmethod
    def delete(topic_id):
        ref = topics_ref.document(topic_id)
        if not ref.get().exists:
            raise NotFound(description="Topic not found")
        
        # CASCADE DELETE
        QuestionService.delete_questions_for_topic(topic_id)

        ref.delete()
        
        return topic_id
