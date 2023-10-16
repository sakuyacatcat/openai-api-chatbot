import os

import openai
from flask import Blueprint, Flask, jsonify, render_template, request

bp = Blueprint("routes", __name__)


def generate_gpt3_response(conversation):
    openai.api_key = os.environ.get("API_KEY")
    model_name = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")

    response = openai.ChatCompletion.create(
        model=model_name, messages=conversation
    )

    return response["choices"][0]["message"]["content"].strip()


@bp.route("/chat", methods=["POST"])
def chat():
    conversation = request.json.get("conversation", [])
    bot_response = generate_gpt3_response(conversation)
    return jsonify({"response": bot_response})


@bp.route("/")
def index():
    return render_template("index.html")
