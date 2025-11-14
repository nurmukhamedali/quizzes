# controllers/card_controller.py

from flask import jsonify, g
from services.card_service import CardService

class CardController:

    @staticmethod
    def list(topic_id):
        cards = CardService.list(g.user["uid"], topic_id)
        return jsonify({"cards": cards})

    @staticmethod
    def get(card_id):
        card = CardService.get(card_id)
        return jsonify(card)

    @staticmethod
    def create(data):
        question_id = data["question_id"]
        new_card = CardService.create(g.user["uid"], question_id)
        return jsonify(new_card), 201

    @staticmethod
    def update_review(card_id, data):
        is_correct = data["is_correct"]
        result = CardService.update_after_answer(card_id, is_correct)
        return jsonify(result)

    @staticmethod
    def delete(card_id):
        CardService.delete(card_id)
        return jsonify({"deleted": card_id})
