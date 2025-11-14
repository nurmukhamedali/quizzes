# models/topic_schema.py

from marshmallow import Schema, fields, validates_schema, ValidationError, EXCLUDE

class TopicSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True, dump_default=None)

    @validates_schema
    def validate_topic(self, data, **kwargs):
        """Structural rule: topic name cannot be blank."""
        topic_name = data.get('name')
        if not topic_name.strip():
            raise ValidationError("Topic name cannot be empty.")
    
    class Meta:
        unknown = EXCLUDE  # Raise error for unknown fields