# middleware/validation.py

from functools import wraps
from flask import request, g 
from marshmallow import ValidationError

def validate_with(schema_class):
    """
    Use as @validate_with(MySchema)
    Validates request.json using given Marshmallow schema.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check content type
            if not request.is_json:
                raise ValidationError({"_schema": ["Content-Type must be application/json"]})
            
            json_data = request.get_json()
            if not json_data:
                raise ValidationError({"_schema": ["Missing JSON body"]})

            schema = schema_class()

            # Let errors bubble up — your global handler will catch them
            validated_data = schema.load(json_data)

            g.validated_data = validated_data
            return f(*args, **kwargs)
        return wrapper
    return decorator