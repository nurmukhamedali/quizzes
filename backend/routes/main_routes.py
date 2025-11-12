from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask Firebase API"})

@main_bp.route('/login', methods=['GET'])
def login_page():
    """Serve the simple Firebase Google Login page."""
    return render_template("login.html")