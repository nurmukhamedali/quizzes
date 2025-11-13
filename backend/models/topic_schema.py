# models/topic_schema.py

from marshmallow import Schema, fields, validates, ValidationError, EXCLUDE

class TopicSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True, dump_default=None)

    @validates("name")
    def validate_name(self, value):
        """Structural rule: topic name cannot be blank."""
        if not value.strip():
            raise ValidationError("Topic name cannot be empty.")
    
    class Meta:
        unknown = EXCLUDE  # Raise error for unknown fields