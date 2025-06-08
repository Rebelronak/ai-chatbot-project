from flask import Blueprint, request, jsonify
from services.nlp_service import process_message

api_routes = Blueprint("api_routes", __name__)

@api_routes.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    bot_response = process_message(user_message)
    return jsonify({"response": bot_response})