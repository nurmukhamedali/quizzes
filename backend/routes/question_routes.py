# routes/question_routes.py

from flask import Blueprint, jsonify, request, g
from middleware.auth_decorators import require_auth, require_role
from middleware.validation import validate_with
from models.question_schema import QuestionSchema
from controllers.question_controller import QuestionController

question_bp = Blueprint("questions", __name__)

# GET ALL quesions
@question_bp.route("/", methods=["GET"])
@require_role("admin")
def list_questions():
        return QuestionController.list()

# CREATE question
@question_bp.route("/", methods=["POST"])
@require_role("admin")
@validate_with(QuestionSchema)
def create_question():
        return QuestionController.create(request.validated_data)

# UPDATE question
@question_bp.route("/<question_id>", methods=["PUT"])
@require_role("admin")
@validate_with(QuestionSchema)
def update_question(question_id):
        return QuestionController.update(question_id, request.validated_data)

# DELETE question
@question_bp.route("/<question_id>", methods=["DELETE"])
@require_auth
@require_role("admin")
def delete_question(question_id):
        return QuestionController.delete(question_id)
