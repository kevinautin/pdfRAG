# from flask import Flask, request, jsonify
# from chatbot import ChatBot
# import time
# import json

# app = Flask(__name__)
# chatbot = ChatBot()
#
#
# @app.route("/ask", methods=["POST"])
# def ask():
#     question = request.json.get("question")
#     start_time = time.time()
#     response = chatbot.answer_question(question)
#     end_time = time.time()
#
#     latency = end_time - start_time
#     save_response(question, response, latency)
#
#     return jsonify({"response": response, "latency": latency})
#
#
# def save_response(question, response, latency):
#     data = {"question": question, "response": response, "latency": latency}
#     with open("responses.json", "a") as f:
#         json.dump(data, f)
#         f.write("\n")
#

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"
db = SQLAlchemy(app)


class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


db.create_all()


def query(question, history):
    # Mock implementation of the query function for illustration
    return f"Response to: {question}"


@app.route("/query", methods=["POST"])
def handle_query():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "Question is required"}), 400

    history = Interaction.query.order_by(Interaction.timestamp).all()
    history_data = [(item.question, item.response) for item in history]

    response = query(question, history_data)

    interaction = Interaction(question=question, response=response)
    db.session.add(interaction)
    db.session.commit()

    return jsonify({"response": response})


@app.route("/history", methods=["GET"])
def get_history():
    history = Interaction.query.order_by(Interaction.timestamp).all()
    history_data = [
        {
            "question": item.question,
            "response": item.response,
            "timestamp": item.timestamp,
        }
        for item in history
    ]
    return jsonify(history_data)


if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run(debug=True)
