from marshmallow import Schema, fields, RAISE

class UserCardSchema(Schema):
    questionId = fields.Str(required=True)
    selectedAnswers = fields.List(fields.Str(), required=True)
    isCorrect = fields.Bool(required=True)

    class Meta:
        unknown = RAISE  # Raise error for unknown fields
