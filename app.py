from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
from call_chatbot import call_chatbot

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"
db = SQLAlchemy(app)


class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=False)
    response_time_s = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def query(question):
    start_time = time.time()
    response = call_chatbot(question)
    response_time_s = time.time() - start_time
    return response, response_time_s


@app.route("/query", methods=["POST"])
def handle_query():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "Question is required"}), 400

    # history = Interaction.query.order_by(Interaction.timestamp).all()
    # history_data = [(item.question, item.response) for item in history]
    # response, response_time_s = query(question, history_data)
    response, response_time_s = query(question)

    interaction = Interaction(
        question=question, response=response, response_time_s=response_time_s
    )
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
            "response_time_s": item.response_time_s,
            "timestamp": item.timestamp,
        }
        for item in history
    ]
    return jsonify(history_data)


@app.route("/history", methods=["DELETE"])
def delete_history():
    try:
        num_deleted = db.session.query(Interaction).delete()
        db.session.commit()
        return jsonify(
            {"message": f"Deleted {num_deleted} interactions from history."}
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
