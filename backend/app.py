from flask import Flask
from config.settings import Config
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG)
