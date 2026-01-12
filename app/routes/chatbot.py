from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.utils.ai_chatbot import get_ai_reply

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chatbot", methods=["GET"])
@login_required
def chatbot_page():
    return render_template("hostel/chatbot.html")

@chatbot_bp.route("/chatbot/message", methods=["POST"])
@login_required
def chatbot_message():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"reply": "⚠️ Invalid request"}), 400

    user_msg = data["message"].strip()

    if not user_msg:
        return jsonify({"reply": "⚠️ Please enter a message"}), 400

    try:
        reply = get_ai_reply(user_msg)
    except Exception as e:
        print(f"[AI ERROR] {e}")
        reply = "⚠️ AI service is temporarily unavailable."

    return jsonify({"reply": reply}), 200
