import os

import openai
from flask import Blueprint, jsonify, request

bp = Blueprint("routes", __name__)


def generate_gpt3_response(
    prompt, max_tokens=1024, n=1, stop=None, temperature=0.5
):
    openai.api_key = os.environ.get("API_KEY")  # 環境変数からAPIキーを取得

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
    )

    return response.choices[0].text.strip()


@bp.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("user_input", "")
    bot_response = generate_gpt3_response(user_input)
    return jsonify({"response": bot_response})
