from flask import Blueprint, jsonify, request, g
from middleware.auth_decorators import require_auth
from middleware.validation import validate_with
from models.card_schema import UserCardSchema
from config.settings import db
from datetime import datetime

card_bp = Blueprint("cards", __name__)
cards_ref = db.collection("cards")

@card_bp.route("/", methods=["GET"])
@require_auth
def list_cards():
        docs = cards_ref.where("userId", "==", g.user["uid"]).stream()
        cards = [dict(doc.to_dict(), id=doc.id) for doc in docs]
        return jsonify({"cards": cards})

@card_bp.route("/", methods=["POST"])
@require_auth
@validate_with(UserCardSchema)
def create_card():
        data = request.validated_data
        data.update({
            "userId": g.user["uid"],
            "submittedAt": datetime.utcnow().isoformat(),
        })

        # unique composite key: userId + questionId
        doc_id = f"{g.user['uid']}_{data['questionId']}"
        cards_ref.document(doc_id).set(data)
        return jsonify({"message": "Answer saved", "id": doc_id}), 201
