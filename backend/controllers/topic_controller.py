# controllers/topic_controller.py

from flask import jsonify, g
from services.topic_service import TopicService

class TopicController:
    @staticmethod
    def list():
        return jsonify({"topics": TopicService.list()})
    
    @staticmethod
    def get(topic_id):
        topic = TopicService.get(topic_id)
        return jsonify(topic)

    @staticmethod
    def create(data):
        new_topic = TopicService.create(data, g.user["uid"])
        return jsonify(new_topic), 201

    @staticmethod
    def update(topic_id, data):
        updated_topic = TopicService.update(topic_id, data)
        return jsonify(updated_topic)

    @staticmethod
    def delete(topic_id):
        TopicService.delete(topic_id)
        return jsonify({"deleted": topic_id})
