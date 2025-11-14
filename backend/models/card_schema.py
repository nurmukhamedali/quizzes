# models/card_schema.py

from marshmallow import Schema, fields, validates_schema, ValidationError, RAISE

class CardSchema(Schema):
    question_id = fields.String(required=True)

    class Meta:
        unknown = RAISE  # Raise error for unknown fields

class ReviewCardSchema(Schema):
    is_correct = fields.Bool(required=True)

    class Meta:
        unknown = RAISE  # Raise error for unknown fields
