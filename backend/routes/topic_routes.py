# routes/topic_routes.py

from flask import Blueprint, request, g
from middleware.auth_decorators import require_auth, require_role
from middleware.validation import validate_with
from models.topic_schema import TopicSchema
from controllers.topic_controller import TopicController

topic_bp = Blueprint('topics', __name__)

# GET ALL topics
@topic_bp.route('/', methods=['GET'])
@require_auth
def list_topics():
        return TopicController.list()

# GET topic
@topic_bp.route('/<topic_id>', methods=['GET'])
@require_auth
def get_topic(topic_id):
        return TopicController.get(topic_id)
    
# CREATE topic
@topic_bp.route('/', methods=['POST'])
@require_role('admin')
@validate_with(TopicSchema)
def create_topic():
        return TopicController.create(g.validated_data)
    
# UPDATE topic
@topic_bp.route('/<topic_id>', methods=['PUT'])
@require_role('admin')
@validate_with(TopicSchema)
def update_topic(topic_id):
        return TopicController.update(topic_id, g.validated_data)
    

# DELETE topic
@topic_bp.route('/<topic_id>', methods=['DELETE'])
@require_role('admin')
def delete_topic(topic_id):
        return TopicController.delete(topic_id)