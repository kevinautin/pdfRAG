from flask import Flask, request, jsonify
from chatbot import ChatBot
import time
import json

app = Flask(__name__)
chatbot = ChatBot()


@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")
    start_time = time.time()
    response = chatbot.answer_question(question)
    end_time = time.time()

    latency = end_time - start_time
    save_response(question, response, latency)

    return jsonify({"response": response, "latency": latency})


def save_response(question, response, latency):
    data = {"question": question, "response": response, "latency": latency}
    with open("responses.json", "a") as f:
        json.dump(data, f)
        f.write("\n")


if __name__ == "__main__":
    app.run(debug=True)
