# middleware/error_handlers.py

from flask import jsonify
from werkzeug.exceptions import BadRequest, HTTPException, NotFound, Forbidden, Unauthorized
from marshmallow import ValidationError

def register_error_handlers(app):
    """Register all error handlers for the Flask app"""

    # ------------- Marshmallow Validation Error -------------
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({
            "error": "VALIDATION_ERROR",
            "details": e.messages
        }), 400
    
    # --------- Python ValueError (Business rule errors) ---------
    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return jsonify({
            "error": "VALUE_ERROR",
            "message": str(e),
        }), 400
    
    # --------- Firestore/NotFound Errors (404) ---------
    @app.errorhandler(NotFound)
    def handle_not_found(e):
        return jsonify({
            "error": "NOT_FOUND",
            "message": e.description if e.description else "Resource not found"
        }), 404

    # ------------- Standard Werkzeug HTTP errors -------------
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "error": e.name.upper().replace(" ", "_"),
            "message": e.description,
        }), e.code
    
    # --------- JSON Parse Errors (BadRequest) ---------
    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return jsonify({
            "error": "BAD_REQUEST",
            "message": str(e)
        }), 400
    
    # ------------- Unauthorized (401) -------------
    @app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return jsonify({
            "success": False,
            "error": "UNAUTHORIZED",
            "message": e.description or "Authentication required"
        }), 401

    # ------------- Forbidden (403) -------------
    @app.errorhandler(Forbidden)
    def handle_forbidden(e):
        return jsonify({
            "success": False,
            "error": "FORBIDDEN",
            "message": e.description or "Permission denied"
        }), 403
    
    # ------------- Catch-All for Unhandled Exceptions -------------
    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        # app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
        return jsonify({
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred"
        }), 500

