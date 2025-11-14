# models/question_schema.py

from marshmallow import Schema, fields, ValidationError, validates_schema, EXCLUDE
import string

class OptionSchema(Schema):
    id = fields.Str(required=True)
    text = fields.Str(required=True)
    images = fields.List(fields.Str(), allow_none=True, load_default=None)    

    @validates_schema
    def validate_option_id(self, data, **kwargs):
        """Validate option id is A-Z"""
        valid_ids = list(string.ascii_uppercase)  # ['A', 'B', 'C', ..., 'Z']
        option_id = data.get('id')
        if option_id not in valid_ids:
            raise ValidationError(f'Option id must be one of: {valid_ids}', field_name='id')

    class Meta:
        unknown = EXCLUDE  # Raise error for unknown fields

class QuestionSchema(Schema):
    topic_id = fields.Str(required=True)
    number = fields.Int(required=True)
    text = fields.Str(required=True)
    type = fields.Str(required=True)
    images = fields.List(fields.Str(), allow_none=True, load_default=None)
    options = fields.List(fields.Nested(OptionSchema), allow_none=True, load_default=None)
    correct_answers = fields.List(fields.Str(), required=True)
    explanation = fields.Str(allow_none=True)

    @validates_schema
    def validate_question(self, data, **kwargs):
        question_type = data.get('type')
        valid_types = ['radio', 'checkbox', 'input']

        # Validate type
        if question_type not in valid_types:
            raise ValidationError(f'Type must be one of: {valid_types}')

    class Meta:
        unknown = EXCLUDE  # Raise error for unknown fields