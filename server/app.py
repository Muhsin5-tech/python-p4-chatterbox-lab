from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.before_first_request
def initialize_db():
    if not Message.query.first():
        default_message = Message(body="Welcome to the message board", username="System")
        db.session.add(default_message)
        db.session.commit()
        
# GET
@app.route('/messages')
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200
# POST
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# PATCH
@app.route('/messages/<int:id>', methods=['PATCH'])
def messages_by_id(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict()), 200

# DELETE
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 200

if __name__ == '__main__':
    app.run(port=5555)
