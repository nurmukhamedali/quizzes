# routes/card_routes.py

from flask import Blueprint, request, g
from middleware.auth_decorators import require_auth
from middleware.validation import validate_with
from models.card_schema import CardSchema, ReviewCardSchema
from controllers.card_controller import CardController


card_bp = Blueprint("cards", __name__)

# LIST cards for user filtered by topic
@card_bp.route("/", methods=["GET"])
@require_auth
def list_cards():
        topic_id = request.args.get("topic_id") # ?topic_id=topic_123
        return CardController.list(topic_id)

# GET card by id
@card_bp.route("/<card_id>", methods=["GET"])
@require_auth
def get_card(card_id):
        return CardController.get(card_id)

# CREATE card (one-to-one per question)
@card_bp.route("/", methods=["POST"])
@require_auth
@validate_with(CardSchema)
def create_card():
        return CardController.create(g.validated_data)

# UPDATE review after answering
@card_bp.route("/<card_id>/review", methods=["POST"])
@require_auth
@validate_with(ReviewCardSchema)
def review_card(card_id):
        return CardController.update_review(card_id, g.validated_data)

# DELETE card
@card_bp.route("/<card_id>", methods=["DELETE"])
@require_auth
def delete_card(card_id):
        return CardController.delete(card_id)
