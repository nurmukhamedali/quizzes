# services/topic_service.py

from config.settings import db
from werkzeug.exceptions import NotFound
from datetime import datetime

topics_ref = db.collection("topics")

class TopicService:
    @staticmethod
    def list():
        return [ dict(doc.to_dict(), id=doc.id) for doc in topics_ref.stream() ]

    @staticmethod
    def create(data, user_id):
        data.update({
            "createdBy": user_id,
            "createdAt": datetime.now().isoformat()
        })
        _, ref = topics_ref.add(data)
        data["id"] = ref.id
        return data

    @staticmethod
    def update(topic_id, data):
        ref = topics_ref.document(topic_id)
        if not ref.get().exists:
            raise NotFound(description="Topic not found")
        ref.update(data)
        return topic_id

    @staticmethod
    def delete(topic_id):
        ref = topics_ref.document(topic_id)
        if not ref.get().exists:
            raise NotFound(description="Topic not found")
        ref.delete()
        return topic_id
