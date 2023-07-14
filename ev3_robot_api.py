import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import openai
from utils import get_model_messages_functions

load_dotenv()
app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_openai():
    # question = request.json['question'] # this can be thought of as function arg.
    api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = api_key
    task = request.json["task"]
    model, messages, functions = get_model_messages_functions(
        task=task
    )
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    return response


if __name__ == "__main__":
    PORT = os.getenv("PORT")
    app.run(host='0.0.0.0', port=int(PORT))