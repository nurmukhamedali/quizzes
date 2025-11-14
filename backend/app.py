from flask import Flask
from config.settings import Config
from middleware.error_handlers import register_error_handlers

# Import routes
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.topic_routes import topic_bp
from routes.card_routes import card_bp
from routes.question_routes import question_bp



def create_app():
    """Factory to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register global error handlers
    register_error_handlers(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    app.register_blueprint(topic_bp, url_prefix="/topics")
    app.register_blueprint(question_bp, url_prefix="/questions")

    app.register_blueprint(card_bp, url_prefix="/cards")


    return app

# If run directly -> development server
if __name__ == "__main__":
    app = create_app()
    # Use 0.0.0.0 in dev to allow external access (containers); remove in locked-down environments
    # app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))
    app.run(debug=Config.DEBUG)
