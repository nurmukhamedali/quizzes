# controllers/question_controller.py

from flask import jsonify, g
from services.question_service import QuestionService

class QuestionController:
    @staticmethod
    def list(topic_id=None):
        questions = QuestionService.list(topic_id)
        return jsonify({"questions": questions})
    
    @staticmethod
    def get(question_id):
        question = QuestionService.get(question_id)
        return jsonify(question)

    @staticmethod
    def create(data):
        new_question = QuestionService.create(data, g.user["uid"])
        return jsonify(new_question), 201
        
        
    @staticmethod
    def update(question_id, data):
        QuestionService.update(question_id, data)
        return jsonify({"message": f"Question {question_id} updated"})

    @staticmethod
    def delete(question_id):
        QuestionService.delete(question_id)
        return jsonify({"message": f"Question {question_id} deleted"})
